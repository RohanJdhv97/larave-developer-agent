# Razorpay Integration for Laravel

## Initialization and Setup

### Required Packages
```php
composer require razorpay/razorpay
```

### Environment Variables
```
RAZORPAY_KEY=rzp_test_your_key
RAZORPAY_SECRET=your_secret_key
RAZORPAY_WEBHOOK_SECRET=your_webhook_secret
```

### Service Provider Registration
Create a service provider:

```php
<?php

namespace App\Providers;

use Illuminate\Support\ServiceProvider;
use Razorpay\Api\Api;

class RazorpayServiceProvider extends ServiceProvider
{
    public function register()
    {
        $this->app->singleton('razorpay', function ($app) {
            return new Api(
                config('services.razorpay.key'),
                config('services.razorpay.secret')
            );
        });
    }

    public function boot()
    {
        // Additional boot logic if needed
    }
}
```

Register in `config/app.php`:
```php
'providers' => [
    // Other providers
    App\Providers\RazorpayServiceProvider::class,
],
```

Update `config/services.php`:
```php
'razorpay' => [
    'key' => env('RAZORPAY_KEY'),
    'secret' => env('RAZORPAY_SECRET'),
    'webhook_secret' => env('RAZORPAY_WEBHOOK_SECRET'),
],
```

## Payment Processing Workflows

### One-Time Payment

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Razorpay\Api\Api;
use Illuminate\Support\Str;

class RazorpayPaymentController extends Controller
{
    protected $razorpay;

    public function __construct(Api $razorpay)
    {
        $this->razorpay = $razorpay;
    }

    public function createOrder(Request $request)
    {
        $receiptId = 'order_' . Str::random(16);
        
        try {
            $order = $this->razorpay->order->create([
                'receipt' => $receiptId,
                'amount' => $request->amount * 100, // Amount in paise
                'currency' => 'INR',
                'notes' => [
                    'order_id' => $request->order_id,
                    'customer_id' => $request->user()->id,
                    'product_name' => $request->product_name
                ]
            ]);
            
            // Save order details to your database
            $payment = new \App\Models\Payment;
            $payment->user_id = $request->user()->id;
            $payment->order_id = $request->order_id;
            $payment->razorpay_order_id = $order->id;
            $payment->amount = $request->amount;
            $payment->status = 'created';
            $payment->save();
            
            return response()->json([
                'success' => true,
                'order' => $order,
                'key' => config('services.razorpay.key')
            ]);
        } catch (\Exception $e) {
            \Log::error('Razorpay order creation failed: ' . $e->getMessage());
            
            return response()->json([
                'success' => false,
                'message' => $e->getMessage()
            ], 500);
        }
    }

    public function verifyPayment(Request $request)
    {
        try {
            $attributes = [
                'razorpay_order_id' => $request->razorpay_order_id,
                'razorpay_payment_id' => $request->razorpay_payment_id,
                'razorpay_signature' => $request->razorpay_signature
            ];
            
            $this->razorpay->utility->verifyPaymentSignature($attributes);
            
            // Update payment status in your database
            $payment = \App\Models\Payment::where('razorpay_order_id', $request->razorpay_order_id)->first();
            if ($payment) {
                $payment->status = 'completed';
                $payment->razorpay_payment_id = $request->razorpay_payment_id;
                $payment->razorpay_signature = $request->razorpay_signature;
                $payment->save();
                
                // Fire event
                event(new \App\Events\PaymentCompleted($payment));
            }
            
            return response()->json([
                'success' => true,
                'message' => 'Payment verified successfully'
            ]);
        } catch (\Exception $e) {
            \Log::error('Razorpay payment verification failed: ' . $e->getMessage());
            
            return response()->json([
                'success' => false,
                'message' => 'Payment verification failed: ' . $e->getMessage()
            ], 400);
        }
    }
}
```

### Subscription Payment

```php
public function createSubscription(Request $request)
{
    try {
        // Create a plan if not exists
        $planId = null;
        try {
            $plans = $this->razorpay->plan->all(['item[id]' => $request->plan_id]);
            if (count($plans->items) > 0) {
                $planId = $plans->items[0]->id;
            } else {
                throw new \Exception('Plan not found');
            }
        } catch (\Exception $e) {
            // Plan doesn't exist, create a new one
            $plan = $this->razorpay->plan->create([
                'period' => $request->period, // 'weekly', 'monthly', 'yearly'
                'interval' => 1,
                'item' => [
                    'name' => $request->plan_name,
                    'description' => $request->plan_description,
                    'amount' => $request->amount * 100,
                    'currency' => 'INR'
                ]
            ]);
            $planId = $plan->id;
        }
        
        // Create a subscription
        $subscription = $this->razorpay->subscription->create([
            'plan_id' => $planId,
            'customer_notify' => 1,
            'total_count' => $request->total_cycles ?? 6, // Number of billing cycles
            'notes' => [
                'user_id' => $request->user()->id,
                'plan_name' => $request->plan_name
            ]
        ]);
        
        // Save subscription details
        $subscriptionModel = new \App\Models\Subscription;
        $subscriptionModel->user_id = $request->user()->id;
        $subscriptionModel->razorpay_subscription_id = $subscription->id;
        $subscriptionModel->razorpay_plan_id = $planId;
        $subscriptionModel->status = $subscription->status;
        $subscriptionModel->plan_name = $request->plan_name;
        $subscriptionModel->amount = $request->amount;
        $subscriptionModel->start_at = now();
        $subscriptionModel->save();
        
        return response()->json([
            'success' => true,
            'subscription' => $subscription
        ]);
    } catch (\Exception $e) {
        \Log::error('Razorpay subscription creation failed: ' . $e->getMessage());
        
        return response()->json([
            'success' => false,
            'message' => $e->getMessage()
        ], 500);
    }
}

public function cancelSubscription(Request $request, $subscriptionId)
{
    try {
        $subscription = $this->razorpay->subscription->fetch($subscriptionId);
        
        // Cancel at end of current period (does not refund)
        $subscription = $this->razorpay->subscription->fetch($subscriptionId)->cancel(true);
        
        // Update subscription in database
        $subscriptionModel = \App\Models\Subscription::where('razorpay_subscription_id', $subscriptionId)->first();
        if ($subscriptionModel) {
            $subscriptionModel->status = 'cancelled';
            $subscriptionModel->cancelled_at = now();
            $subscriptionModel->save();
        }
        
        return response()->json([
            'success' => true,
            'message' => 'Subscription cancelled successfully'
        ]);
    } catch (\Exception $e) {
        \Log::error('Razorpay subscription cancellation failed: ' . $e->getMessage());
        
        return response()->json([
            'success' => false,
            'message' => $e->getMessage()
        ], 500);
    }
}
```

## Webhooks and Callbacks

### Webhook Controller

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Log;

class RazorpayWebhookController extends Controller
{
    public function handleWebhook(Request $request)
    {
        // Verify webhook signature
        $payload = $request->getContent();
        $signature = $request->header('X-Razorpay-Signature');
        $webhookSecret = config('services.razorpay.webhook_secret');
        
        try {
            $this->verifySignature($payload, $signature, $webhookSecret);
        } catch (\Exception $e) {
            Log::error('Razorpay webhook signature verification failed: ' . $e->getMessage());
            return response()->json(['error' => 'Webhook signature verification failed'], 400);
        }
        
        $data = json_decode($payload, true);
        $event = $data['event'];
        
        Log::info('Razorpay webhook received: ' . $event);
        
        switch ($event) {
            case 'payment.authorized':
                $this->handlePaymentAuthorized($data['payload']['payment']['entity']);
                break;
            
            case 'payment.failed':
                $this->handlePaymentFailed($data['payload']['payment']['entity']);
                break;
            
            case 'order.paid':
                $this->handleOrderPaid($data['payload']['order']['entity']);
                break;
            
            case 'subscription.activated':
                $this->handleSubscriptionActivated($data['payload']['subscription']['entity']);
                break;
            
            case 'subscription.charged':
                $this->handleSubscriptionCharged($data['payload']['subscription']['entity'], 
                                                 $data['payload']['payment']['entity']);
                break;
            
            case 'subscription.halted':
                $this->handleSubscriptionHalted($data['payload']['subscription']['entity']);
                break;
            
            case 'subscription.cancelled':
                $this->handleSubscriptionCancelled($data['payload']['subscription']['entity']);
                break;
            
            default:
                Log::info('Unhandled Razorpay webhook event: ' . $event);
        }
        
        return response()->json(['status' => 'received']);
    }
    
    private function verifySignature($payload, $signature, $secret)
    {
        $expectedSignature = hash_hmac('sha256', $payload, $secret);
        if ($expectedSignature !== $signature) {
            throw new \Exception('Invalid webhook signature');
        }
    }
    
    private function handlePaymentAuthorized($payment)
    {
        Log::info('Payment authorized: ' . $payment['id']);
        
        // Find the payment in your database
        $paymentModel = \App\Models\Payment::where('razorpay_order_id', $payment['order_id'])
            ->orWhere('razorpay_payment_id', $payment['id'])
            ->first();
        
        if ($paymentModel) {
            $paymentModel->status = 'authorized';
            $paymentModel->razorpay_payment_id = $payment['id'];
            $paymentModel->save();
            
            // Process your business logic
            // Update order status, send notification, etc.
        }
    }
    
    private function handlePaymentFailed($payment)
    {
        Log::error('Payment failed: ' . $payment['id'] . ', Error: ' . 
            ($payment['error_code'] ?? 'unknown') . ' - ' . 
            ($payment['error_description'] ?? 'unknown'));
        
        // Find the payment in your database
        $paymentModel = \App\Models\Payment::where('razorpay_order_id', $payment['order_id'])
            ->orWhere('razorpay_payment_id', $payment['id'])
            ->first();
        
        if ($paymentModel) {
            $paymentModel->status = 'failed';
            $paymentModel->error_code = $payment['error_code'] ?? null;
            $paymentModel->error_description = $payment['error_description'] ?? null;
            $paymentModel->save();
            
            // Process your business logic
            // Notify the user, reset inventory, etc.
        }
    }
    
    private function handleOrderPaid($order)
    {
        Log::info('Order paid: ' . $order['id']);
        
        // Find the payment in your database
        $paymentModel = \App\Models\Payment::where('razorpay_order_id', $order['id'])->first();
        
        if ($paymentModel) {
            $paymentModel->status = 'completed';
            $paymentModel->save();
            
            // Process your business logic
            // Fulfill order, send confirmation, etc.
        }
    }
    
    private function handleSubscriptionActivated($subscription)
    {
        Log::info('Subscription activated: ' . $subscription['id']);
        
        // Find the subscription in your database
        $subscriptionModel = \App\Models\Subscription::where('razorpay_subscription_id', $subscription['id'])->first();
        
        if ($subscriptionModel) {
            $subscriptionModel->status = 'active';
            $subscriptionModel->save();
            
            // Process your business logic
            // Provide access to subscription features, etc.
        }
    }
    
    private function handleSubscriptionCharged($subscription, $payment)
    {
        Log::info('Subscription charged: ' . $subscription['id'] . ', Payment: ' . $payment['id']);
        
        // Find the subscription in your database
        $subscriptionModel = \App\Models\Subscription::where('razorpay_subscription_id', $subscription['id'])->first();
        
        if ($subscriptionModel) {
            // Create a subscription payment record
            $paymentModel = new \App\Models\SubscriptionPayment;
            $paymentModel->subscription_id = $subscriptionModel->id;
            $paymentModel->razorpay_payment_id = $payment['id'];
            $paymentModel->amount = $payment['amount'] / 100;
            $paymentModel->status = 'completed';
            $paymentModel->paid_at = now();
            $paymentModel->save();
            
            // Process your business logic
            // Update subscription period, send receipt, etc.
        }
    }
    
    private function handleSubscriptionHalted($subscription)
    {
        Log::warning('Subscription halted: ' . $subscription['id']);
        
        // Find the subscription in your database
        $subscriptionModel = \App\Models\Subscription::where('razorpay_subscription_id', $subscription['id'])->first();
        
        if ($subscriptionModel) {
            $subscriptionModel->status = 'halted';
            $subscriptionModel->save();
            
            // Process your business logic
            // Notify the user, restrict access, etc.
        }
    }
    
    private function handleSubscriptionCancelled($subscription)
    {
        Log::info('Subscription cancelled: ' . $subscription['id']);
        
        // Find the subscription in your database
        $subscriptionModel = \App\Models\Subscription::where('razorpay_subscription_id', $subscription['id'])->first();
        
        if ($subscriptionModel) {
            $subscriptionModel->status = 'cancelled';
            $subscriptionModel->cancelled_at = now();
            $subscriptionModel->save();
            
            // Process your business logic
            // Revoke access, send confirmation, etc.
        }
    }
}
```

### Route Registration

```php
// Register webhook routes
Route::post(
    'razorpay/webhook',
    [\App\Http\Controllers\RazorpayWebhookController::class, 'handleWebhook']
)->name('razorpay.webhook');

// Register payment routes
Route::middleware(['auth'])->group(function () {
    Route::post(
        'razorpay/create-order',
        [\App\Http\Controllers\RazorpayPaymentController::class, 'createOrder']
    )->name('razorpay.create-order');
    
    Route::post(
        'razorpay/verify-payment',
        [\App\Http\Controllers\RazorpayPaymentController::class, 'verifyPayment']
    )->name('razorpay.verify-payment');
    
    Route::post(
        'razorpay/create-subscription',
        [\App\Http\Controllers\RazorpayPaymentController::class, 'createSubscription']
    )->name('razorpay.create-subscription');
    
    Route::post(
        'razorpay/cancel-subscription/{id}',
        [\App\Http\Controllers\RazorpayPaymentController::class, 'cancelSubscription']
    )->name('razorpay.cancel-subscription');
});
```

## Error Handling Patterns

```php
try {
    // Razorpay API call
} catch (\Razorpay\Api\Errors\BadRequestError $e) {
    // Invalid parameters were supplied to Razorpay's API
    \Log::error('Razorpay Bad Request Error: ' . $e->getMessage());
    return response()->json([
        'error' => 'Invalid payment information. Please check your details.',
        'details' => $e->getMessage()
    ], 400);
} catch (\Razorpay\Api\Errors\GatewayError $e) {
    // Payment gateway error
    \Log::error('Razorpay Gateway Error: ' . $e->getMessage());
    return response()->json([
        'error' => 'Payment gateway error. Please try again later.',
        'details' => $e->getMessage()
    ], 502);
} catch (\Razorpay\Api\Errors\ServerError $e) {
    // Razorpay server error
    \Log::error('Razorpay Server Error: ' . $e->getMessage());
    return response()->json([
        'error' => 'Razorpay server error. Please try again later.',
        'details' => $e->getMessage()
    ], 500);
} catch (\Exception $e) {
    // Something else happened, completely unrelated to Razorpay
    \Log::error('General Error: ' . $e->getMessage());
    return response()->json([
        'error' => 'An unexpected error occurred. Please try again later.',
        'details' => $e->getMessage()
    ], 500);
}
```

## Security Best Practices

1. **Verify signatures for all callbacks and webhooks**:
   ```php
   // Verify payment signature
   $attributes = [
       'razorpay_order_id' => $request->razorpay_order_id,
       'razorpay_payment_id' => $request->razorpay_payment_id,
       'razorpay_signature' => $request->razorpay_signature
   ];
   
   try {
       $this->razorpay->utility->verifyPaymentSignature($attributes);
       // Signature is valid, process the payment
   } catch (\Exception $e) {
       // Signature verification failed
       return response()->json(['error' => 'Invalid signature'], 400);
   }
   ```

2. **Never store sensitive payment information**:
   - Avoid storing card data on your server
   - Use Razorpay's hosted checkout or secure integration methods

3. **Use HTTPS for all payment pages**:
   ```php
   // In AppServiceProvider.php
   public function boot()
   {
       if(config('app.env') === 'production') {
           \URL::forceScheme('https');
       }
   }
   ```

4. **Implement proper validation**:
   ```php
   $request->validate([
       'amount' => 'required|numeric|min:1',
       'currency' => 'required|string|in:INR',
       'razorpay_payment_id' => 'required|string|max:255',
       'razorpay_order_id' => 'required|string|max:255',
       'razorpay_signature' => 'required|string|max:255',
   ]);
   ```

5. **Secure your API keys and secrets**:
   - Store all sensitive credentials in .env file
   - Ensure webhook secret is properly secured
   - Regularly rotate your keys

## Testing and Debugging

### Test Mode

Always use test mode in development and testing environments:

```php
// Check if using test mode and set appropriate keys
$isTestMode = app()->environment('local', 'testing');

if ($isTestMode) {
    // Test credentials
    $key = config('services.razorpay.test_key');
    $secret = config('services.razorpay.test_secret');
} else {
    // Production credentials
    $key = config('services.razorpay.key');
    $secret = config('services.razorpay.secret');
}

$razorpay = new \Razorpay\Api\Api($key, $secret);
```

### Test Cards

Use these test card numbers for testing:

| Card Type | Card Number | Expiry | CVV |
|-----------|-------------|--------|-----|
| Visa (Success) | 4111 1111 1111 1111 | Any future date | Any 3 digits |
| MasterCard (Success) | 5267 3181 8797 5449 | Any future date | Any 3 digits |
| MasterCard (Failure) | 5268 9406 2983 9313 | Any future date | Any 3 digits |

### Debugging Tips

1. **Enable Razorpay Debug Mode**:
   ```php
   // In your service provider
   public function register()
   {
       $this->app->singleton('razorpay', function ($app) {
           $api = new Api(
               config('services.razorpay.key'),
               config('services.razorpay.secret')
           );
           if (config('app.debug')) {
               $api->setDebug(true);
           }
           return $api;
       });
   }
   ```

2. **Log All Requests and Responses**:
   ```php
   // Create a middleware for logging
   public function handle($request, Closure $next)
   {
       if (Str::startsWith($request->path(), 'razorpay')) {
           \Log::debug('Razorpay Request: ' . $request->path(), [
               'method' => $request->method(),
               'params' => $request->except(['card']),
           ]);
       }
       
       $response = $next($request);
       
       if (Str::startsWith($request->path(), 'razorpay')) {
           \Log::debug('Razorpay Response: ' . $request->path(), [
               'status' => $response->status(),
           ]);
       }
       
       return $response;
   }
   ```

3. **Simulate Webhooks Locally**:
   - Use the Razorpay Test Dashboard to trigger test webhooks
   - Or manually create webhook payloads for testing

## Integration with Filament

### Payment Model

```php
namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Factories\HasFactory;

class Payment extends Model
{
    use HasFactory;
    
    protected $fillable = [
        'user_id',
        'order_id',
        'razorpay_order_id',
        'razorpay_payment_id',
        'razorpay_signature',
        'amount',
        'currency',
        'status',
        'error_code',
        'error_description',
    ];
    
    public function user()
    {
        return $this->belongsTo(User::class);
    }
    
    public function order()
    {
        return $this->belongsTo(Order::class);
    }
}
```

### Filament Resource

```php
namespace App\Filament\Resources;

use App\Filament\Resources\PaymentResource\Pages;
use App\Models\Payment;
use Filament\Forms;
use Filament\Resources\Form;
use Filament\Resources\Resource;
use Filament\Resources\Table;
use Filament\Tables;

class PaymentResource extends Resource
{
    protected static ?string $model = Payment::class;
    protected static ?string $navigationIcon = 'heroicon-o-currency-rupee';
    protected static ?string $navigationGroup = 'Finance';
    
    public static function form(Form $form): Form
    {
        return $form
            ->schema([
                Forms\Components\Card::make()
                    ->schema([
                        Forms\Components\TextInput::make('razorpay_order_id')
                            ->label('Razorpay Order ID')
                            ->disabled(),
                        
                        Forms\Components\TextInput::make('razorpay_payment_id')
                            ->label('Razorpay Payment ID')
                            ->disabled(),
                        
                        Forms\Components\TextInput::make('amount')
                            ->required()
                            ->numeric()
                            ->disabled(),
                        
                        Forms\Components\TextInput::make('currency')
                            ->required()
                            ->default('INR')
                            ->disabled(),
                        
                        Forms\Components\Select::make('status')
                            ->options([
                                'created' => 'Created',
                                'authorized' => 'Authorized',
                                'completed' => 'Completed',
                                'failed' => 'Failed',
                                'refunded' => 'Refunded',
                            ])
                            ->required(),
                        
                        Forms\Components\TextInput::make('error_code')
                            ->disabled(),
                        
                        Forms\Components\Textarea::make('error_description')
                            ->disabled(),
                    ])
            ]);
    }
    
    public static function table(Table $table): Table
    {
        return $table
            ->columns([
                Tables\Columns\TextColumn::make('id')
                    ->label('ID')
                    ->sortable(),
                
                Tables\Columns\TextColumn::make('user.name')
                    ->label('Customer')
                    ->searchable()
                    ->sortable(),
                
                Tables\Columns\TextColumn::make('order_id')
                    ->label('Order ID')
                    ->searchable(),
                
                Tables\Columns\TextColumn::make('amount')
                    ->money('inr')
                    ->sortable(),
                
                Tables\Columns\BadgeColumn::make('status')
                    ->colors([
                        'danger' => 'failed',
                        'warning' => 'created',
                        'success' => 'completed',
                        'primary' => 'authorized',
                    ]),
                
                Tables\Columns\TextColumn::make('created_at')
                    ->dateTime()
                    ->sortable(),
            ])
            ->filters([
                Tables\Filters\SelectFilter::make('status')
                    ->options([
                        'created' => 'Created',
                        'authorized' => 'Authorized',
                        'completed' => 'Completed',
                        'failed' => 'Failed',
                        'refunded' => 'Refunded',
                    ]),
            ])
            ->actions([
                Tables\Actions\ViewAction::make(),
                Tables\Actions\EditAction::make(),
                Tables\Actions\Action::make('refund')
                    ->label('Refund')
                    ->icon('heroicon-o-reply')
                    ->color('warning')
                    ->visible(fn (Payment $record) => $record->status === 'completed')
                    ->action(function (Payment $record) {
                        // Process refund
                        try {
                            $razorpay = app('razorpay');
                            $refund = $razorpay->refund->create([
                                'payment_id' => $record->razorpay_payment_id,
                                'amount' => $record->amount * 100, // in paise
                                'notes' => [
                                    'reason' => 'Customer requested refund',
                                    'refunded_by' => auth()->user()->name,
                                ]
                            ]);
                            
                            $record->status = 'refunded';
                            $record->save();
                            
                            // Notify user about the refund
                            
                            return notification()
                                ->success('Payment refunded successfully')
                                ->send();
                        } catch (\Exception $e) {
                            return notification()
                                ->danger('Refund failed: ' . $e->getMessage())
                                ->send();
                        }
                    }),
            ])
            ->bulkActions([
                Tables\Actions\DeleteBulkAction::make(),
            ]);
    }
    
    public static function getRelations(): array
    {
        return [
            //
        ];
    }
    
    public static function getPages(): array
    {
        return [
            'index' => Pages\ListPayments::route('/'),
            'create' => Pages\CreatePayment::route('/create'),
            'view' => Pages\ViewPayment::route('/{record}'),
            'edit' => Pages\EditPayment::route('/{record}/edit'),
        ];
    }
}
```

### Frontend Integration with Blade

```html
<div class="razorpay-payment-form">
    <form action="{{ route('razorpay.verify-payment') }}" method="POST" id="razorpay-payment-form">
        @csrf
        <input type="hidden" name="razorpay_payment_id" id="razorpay_payment_id">
        <input type="hidden" name="razorpay_order_id" id="razorpay_order_id">
        <input type="hidden" name="razorpay_signature" id="razorpay_signature">
        
        <button type="button" id="razorpay-pay-button" class="btn btn-primary">
            Pay with Razorpay
        </button>
    </form>
</div>

@push('scripts')
<script src="https://checkout.razorpay.com/v1/checkout.js"></script>
<script>
    const options = {
        key: "{{ config('services.razorpay.key') }}",
        amount: "{{ $order->amount * 100 }}", // in paise
        currency: "INR",
        name: "{{ config('app.name') }}",
        description: "Payment for Order #{{ $order->id }}",
        order_id: "{{ $razorpayOrder->id }}",
        handler: function (response) {
            document.getElementById('razorpay_payment_id').value = response.razorpay_payment_id;
            document.getElementById('razorpay_order_id').value = response.razorpay_order_id;
            document.getElementById('razorpay_signature').value = response.razorpay_signature;
            
            // Submit the form
            document.getElementById('razorpay-payment-form').submit();
        },
        prefill: {
            name: "{{ auth()->user()->name }}",
            email: "{{ auth()->user()->email }}",
            contact: "{{ auth()->user()->phone ?? '' }}"
        },
        notes: {
            order_id: "{{ $order->id }}",
            customer_id: "{{ auth()->id() }}"
        },
        theme: {
            color: "#3399cc"
        },
        modal: {
            ondismiss: function() {
                console.log('Payment cancelled');
            }
        }
    };
    
    const razorpay = new Razorpay(options);
    
    document.getElementById('razorpay-pay-button').onclick = function(e) {
        razorpay.open();
        e.preventDefault();
    };
</script>
@endpush 