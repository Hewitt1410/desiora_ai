from fastapi import APIRouter, Request, HTTPException, status, Header, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.core.database import get_db
from app.services.subscription_service import SubscriptionService
from app.models.subscription import SubscriptionStatus, SubscriptionPlan, BillingProvider
from datetime import datetime
import json

router = APIRouter(prefix="/webhooks", tags=["webhooks"])


@router.post("/stripe")
async def stripe_webhook(
    request: Request,
    stripe_signature: Optional[str] = Header(None, alias="stripe-signature"),
    db: AsyncSession = Depends(get_db),
):
    """
    Handle Stripe webhook events.
    
    Supported events:
    - customer.subscription.created
    - customer.subscription.updated
    - customer.subscription.deleted
    - invoice.payment_succeeded
    - invoice.payment_failed
    """
    try:
        # In production, verify webhook signature
        # import stripe
        # event = stripe.Webhook.construct_event(
        #     payload, stripe_signature, settings.STRIPE_WEBHOOK_SECRET
        # )
        
        body = await request.json()
        event_type = body.get("type")
        data = body.get("data", {}).get("object", {})
        
        subscription_service = SubscriptionService(db)
        
        if event_type in [
            "customer.subscription.created",
            "customer.subscription.updated",
            "invoice.payment_succeeded",
        ]:
            subscription_id = data.get("id")
            customer_id = data.get("customer")
            status_str = data.get("status", "active")
            
            # Map Stripe status to our status
            status_mapping = {
                "active": SubscriptionStatus.ACTIVE,
                "canceled": SubscriptionStatus.CANCELED,
                "past_due": SubscriptionStatus.PAST_DUE,
                "trialing": SubscriptionStatus.TRIAL,
            }
            subscription_status = status_mapping.get(status_str, SubscriptionStatus.ACTIVE)
            
            # Get plan from metadata or price
            plan = SubscriptionPlan.MONTHLY  # Default, should be determined from price/plan
            if "metadata" in data and "plan" in data["metadata"]:
                plan_str = data["metadata"]["plan"].lower()
                if plan_str == "weekly":
                    plan = SubscriptionPlan.WEEKLY
                elif plan_str == "yearly":
                    plan = SubscriptionPlan.YEARLY
            
            # Get period end
            period_end = None
            if "current_period_end" in data:
                period_end = datetime.fromtimestamp(data["current_period_end"])
            
            # Find or update subscription
            from app.repositories.subscription_repository import SubscriptionRepository
            subscription_repo = SubscriptionRepository(db)
            subscription = await subscription_repo.get_by_provider_id(
                subscription_id
            )
            
            if subscription:
                await subscription_service.update_subscription_from_webhook(
                    subscription_id,
                    status=subscription_status,
                    plan=plan,
                    period_end=period_end,
                )
            else:
                # Create new subscription (would need user_id from customer_id)
                # This is a simplified example - in production, map customer_id to user_id
                pass
        
        elif event_type == "customer.subscription.deleted":
            subscription_id = data.get("id")
            from app.repositories.subscription_repository import SubscriptionRepository
            subscription_repo = SubscriptionRepository(db)
            subscription = await subscription_repo.get_by_provider_id(
                subscription_id
            )
            if subscription:
                await subscription_service.update_subscription_from_webhook(
                    subscription_id,
                    status=SubscriptionStatus.CANCELED,
                )
        
        elif event_type == "invoice.payment_failed":
            subscription_id = data.get("subscription")
            if subscription_id:
                await subscription_service.update_subscription_from_webhook(
                    subscription_id,
                    status=SubscriptionStatus.PAST_DUE,
                )
        
        return {"received": True, "event_type": event_type}
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Webhook processing failed: {str(e)}"
        )


@router.post("/app-store")
async def app_store_webhook(
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """
    Handle App Store webhook events (Server-to-Server Notification).
    
    Supported notification types:
    - INITIAL_BUY
    - DID_RENEW
    - DID_FAIL_TO_RENEW
    - CANCEL
    - REFUND
    """
    try:
        body = await request.json()
        notification_type = body.get("notification_type")
        unified_receipt = body.get("unified_receipt", {})
        latest_receipt_info = unified_receipt.get("latest_receipt_info", [])
        
        if not latest_receipt_info:
            return {"received": True}
        
        receipt = latest_receipt_info[0]
        original_transaction_id = receipt.get("original_transaction_id")
        product_id = receipt.get("product_id")
        
        subscription_service = SubscriptionService(db)
        
        # Map product_id to plan
        plan_mapping = {
            "weekly": SubscriptionPlan.WEEKLY,
            "monthly": SubscriptionPlan.MONTHLY,
            "yearly": SubscriptionPlan.YEARLY,
        }
        plan = plan_mapping.get(product_id.lower(), SubscriptionPlan.MONTHLY)
        
        # Map notification type to status
        if notification_type in ["INITIAL_BUY", "DID_RENEW"]:
            subscription_status = SubscriptionStatus.ACTIVE
        elif notification_type == "DID_FAIL_TO_RENEW":
            subscription_status = SubscriptionStatus.PAST_DUE
        elif notification_type in ["CANCEL", "REFUND"]:
            subscription_status = SubscriptionStatus.CANCELED
        else:
            subscription_status = SubscriptionStatus.ACTIVE
        
        # Get expiration date
        expires_date_ms = receipt.get("expires_date_ms")
        period_end = None
        if expires_date_ms:
            period_end = datetime.fromtimestamp(int(expires_date_ms) / 1000)
        
        # Find subscription by original_transaction_id
        # In production, you'd need to store this mapping
        from app.repositories.subscription_repository import SubscriptionRepository
        subscription_repo = SubscriptionRepository(db)
        subscription = await subscription_repo.get_by_provider_id(
            original_transaction_id
        )
        
        if subscription:
            await subscription_service.update_subscription_from_webhook(
                original_transaction_id,
                status=subscription_status,
                plan=plan,
                period_end=period_end,
            )
        
        return {"received": True, "notification_type": notification_type}
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Webhook processing failed: {str(e)}"
        )


@router.post("/google-play")
async def google_play_webhook(
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """
    Handle Google Play webhook events (Real-time Developer Notifications).
    
    Supported notification types:
    - SUBSCRIPTION_PURCHASED
    - SUBSCRIPTION_RENEWED
    - SUBSCRIPTION_IN_GRACE_PERIOD
    - SUBSCRIPTION_CANCELED
    - SUBSCRIPTION_ON_HOLD
    """
    try:
        body = await request.json()
        message = body.get("message", {})
        data = message.get("data", "")
        
        # Decode base64 data if needed
        import base64
        decoded_data = json.loads(base64.b64decode(data).decode())
        
        subscription_notification = decoded_data.get("subscriptionNotification", {})
        notification_type = subscription_notification.get("notificationType")
        purchase_token = subscription_notification.get("purchaseToken")
        subscription_id = subscription_notification.get("subscriptionId")
        
        subscription_service = SubscriptionService(db)
        
        # Map notification type to status
        status_mapping = {
            1: SubscriptionStatus.ACTIVE,  # SUBSCRIPTION_RECOVERED
            2: SubscriptionStatus.ACTIVE,  # SUBSCRIPTION_RENEWED
            3: SubscriptionStatus.PAST_DUE,  # SUBSCRIPTION_IN_GRACE_PERIOD
            4: SubscriptionStatus.CANCELED,  # SUBSCRIPTION_CANCELED
            5: SubscriptionStatus.PAST_DUE,  # SUBSCRIPTION_ON_HOLD
        }
        subscription_status = status_mapping.get(notification_type, SubscriptionStatus.ACTIVE)
        
        # Map subscription_id to plan
        plan_mapping = {
            "weekly": SubscriptionPlan.WEEKLY,
            "monthly": SubscriptionPlan.MONTHLY,
            "yearly": SubscriptionPlan.YEARLY,
        }
        plan = plan_mapping.get(subscription_id.lower(), SubscriptionPlan.MONTHLY)
        
        # Find subscription by purchase_token
        from app.repositories.subscription_repository import SubscriptionRepository
        subscription_repo = SubscriptionRepository(db)
        subscription = await subscription_repo.get_by_provider_id(
            purchase_token
        )
        
        if subscription:
            await subscription_service.update_subscription_from_webhook(
                purchase_token,
                status=subscription_status,
                plan=plan,
            )
        
        return {"received": True, "notification_type": notification_type}
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Webhook processing failed: {str(e)}"
        )

