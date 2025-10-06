import { headers } from 'next/headers';
import Stripe from 'stripe';

export async function POST(req: Request) {
  const sig = (await headers()).get('stripe-signature');
  const secret = process.env.STRIPE_WEBHOOK_SECRET;
  if (!secret || !sig) return new Response('no sig', { status: 400 });
  const stripe = new Stripe(process.env.STRIPE_SECRET_KEY || 'sk_test_x', { apiVersion: '2024-06-20' });
  const buf = Buffer.from(await req.arrayBuffer());
  let event: Stripe.Event;
  try {
    event = stripe.webhooks.constructEvent(buf, sig, secret);
  } catch (e) {
    return new Response('invalid sig', { status: 400 });
  }
  console.log('Stripe event', event.type);
  return new Response('ok');
}
