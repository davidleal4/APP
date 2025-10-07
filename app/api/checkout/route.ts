import Stripe from 'stripe';

export async function POST() {
  if (!process.env.STRIPE_SECRET_KEY) {
    return Response.json({ url: '#' });
  }
  const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, { apiVersion: '2024-06-20' });
  const session = await stripe.checkout.sessions.create({
    mode: 'subscription',
    line_items: [{ price: 'price_test_pro', quantity: 1 }],
    success_url: 'http://localhost:3000/billing?success=1',
    cancel_url: 'http://localhost:3000/billing?canceled=1'
  });
  return Response.json({ url: session.url });
}
