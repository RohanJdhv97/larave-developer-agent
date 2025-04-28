# Mailgun Email Integration for Laravel

## Initialization and Setup

### Required Packages
```php
composer require symfony/mailgun-mailer symfony/http-client
```

### Environment Variables
```
MAIL_MAILER=mailgun
MAILGUN_DOMAIN=your-domain.com
MAILGUN_SECRET=your-mailgun-api-key
MAILGUN_ENDPOINT=api.mailgun.net  # or api.eu.mailgun.net for EU region
```

### Configuration
Update your `config/mail.php` configuration:

```php
'mailers' => [
    // Other mailers...
    
    'mailgun' => [
        'transport' => 'mailgun',
        'domain' => env('MAILGUN_DOMAIN'),
        'secret' => env('MAILGUN_SECRET'),
        'endpoint' => env('MAILGUN_ENDPOINT', 'api.mailgun.net'),
        'scheme' => 'https',
    ],
],
```

## Basic Email Sending

### Using the Mail Facade

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Mail;
use App\Mail\WelcomeEmail;

class UserController extends Controller
{
    public function sendWelcomeEmail(Request $request)
    {
        $user = $request->user();
        
        try {
            Mail::to($user->email)->send(new WelcomeEmail($user));
            
            return response()->json([
                'success' => true,
                'message' => 'Welcome email sent successfully'
            ]);
        } catch (\Exception $e) {
            \Log::error('Failed to send welcome email: ' . $e->getMessage());
            
            return response()->json([
                'success' => false,
                'message' => 'Failed to send welcome email'
            ], 500);
        }
    }
}
```

### Creating a Mailable Class

```php
<?php

namespace App\Mail;

use Illuminate\Bus\Queueable;
use Illuminate\Mail\Mailable;
use Illuminate\Queue\SerializesModels;
use App\Models\User;

class WelcomeEmail extends Mailable
{
    use Queueable, SerializesModels;

    /**
     * The user instance.
     *
     * @var \App\Models\User
     */
    public $user;

    /**
     * Create a new message instance.
     *
     * @param  \App\Models\User  $user
     * @return void
     */
    public function __construct(User $user)
    {
        $this->user = $user;
    }

    /**
     * Build the message.
     *
     * @return $this
     */
    public function build()
    {
        return $this->subject('Welcome to ' . config('app.name'))
                    ->view('emails.welcome')
                    ->with([
                        'name' => $this->user->name,
                        'verificationUrl' => url('/verify-email/' . $this->user->verification_token),
                    ]);
    }
}
```

### Creating Blade Email Template

```html
<!-- resources/views/emails/welcome.blade.php -->
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Welcome to {{ config('app.name') }}</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
        }
        .header {
            text-align: center;
            padding: 20px 0;
            border-bottom: 1px solid #eee;
        }
        .content {
            padding: 20px 0;
        }
        .button {
            display: inline-block;
            background-color: #3490dc;
            color: white;
            text-decoration: none;
            padding: 10px 20px;
            border-radius: 4px;
            margin-top: 20px;
        }
        .footer {
            padding-top: 20px;
            border-top: 1px solid #eee;
            text-align: center;
            font-size: 0.8em;
            color: #777;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Welcome to {{ config('app.name') }}!</h1>
    </div>
    
    <div class="content">
        <p>Hello {{ $name }},</p>
        
        <p>Thank you for joining {{ config('app.name') }}. We're excited to have you on board!</p>
        
        <p>Please verify your email address by clicking the button below:</p>
        
        <a href="{{ $verificationUrl }}" class="button">Verify Email Address</a>
        
        <p>If you have any questions or need assistance, please don't hesitate to contact our support team.</p>
        
        <p>Best regards,<br>The {{ config('app.name') }} Team</p>
    </div>
    
    <div class="footer">
        <p>© {{ date('Y') }} {{ config('app.name') }}. All rights reserved.</p>
        <p>
            You're receiving this email because you signed up for {{ config('app.name') }}.
            If you'd like to unsubscribe, <a href="{{ url('/unsubscribe/' . $user->unsubscribe_token) }}">click here</a>.
        </p>
    </div>
</body>
</html>
```

## Advanced Email Features

### Adding Attachments

```php
public function build()
{
    return $this->subject('Your Invoice')
                ->view('emails.invoice')
                ->with([
                    'invoiceData' => $this->invoice,
                ])
                ->attach(storage_path('app/invoices/' . $this->invoice->number . '.pdf'), [
                    'as' => 'invoice-' . $this->invoice->number . '.pdf',
                    'mime' => 'application/pdf',
                ]);
}
```

### Adding Inline Attachments

```php
public function build()
{
    return $this->subject('Your Monthly Report')
                ->view('emails.report')
                ->with([
                    'reportData' => $this->report,
                ])
                ->attachData(
                    $this->generateChart(), 
                    'chart.png', 
                    [
                        'mime' => 'image/png',
                        'as' => 'chart.png',
                    ]
                )
                ->embed(public_path('images/logo.png'), 'logo');
}
```

### Using with Blade:

```html
<img src="{{ $message->embedData($chartData, 'chart.png') }}">
<!-- Or if embedded in the build method -->
<img src="{{ $message->embed($logo) }}">
```

### Adding Custom Headers

```php
public function build()
{
    return $this->subject('Your Order Confirmation')
                ->view('emails.order-confirmation')
                ->withSwiftMessage(function ($message) {
                    $message->getHeaders()
                            ->addTextHeader('X-Custom-Header', 'Custom Value')
                            ->addTextHeader('X-Mailgun-Tag', 'order-confirmation')
                            ->addTextHeader('X-Mailgun-Track-Clicks', 'yes')
                            ->addTextHeader('X-Mailgun-Track-Opens', 'yes');
                });
}
```

### Mailgun-Specific Features

```php
public function build()
{
    return $this->subject('Important Announcement')
                ->view('emails.announcement')
                ->withSwiftMessage(function ($message) {
                    $message->getHeaders()
                            ->addTextHeader('X-Mailgun-Variables', json_encode([
                                'user_id' => $this->user->id,
                                'campaign_id' => 'announcement-2023',
                            ]))
                            ->addTextHeader('X-Mailgun-Tag', ['announcement', 'important'])
                            ->addTextHeader('X-Mailgun-Delivery-Time', '3 hours');
                });
}
```

## Email Template Design

### Components-Based Email Design

Create reusable components for emails:

```php
// resources/views/components/email/button.blade.php
<table width="100%" border="0" cellspacing="0" cellpadding="0">
    <tr>
        <td align="center">
            <table border="0" cellspacing="0" cellpadding="0">
                <tr>
                    <td align="center" bgcolor="{{ $color ?? '#3490dc' }}" style="border-radius: 4px;">
                        <a href="{{ $url }}" target="_blank" style="font-size: 16px; font-family: Arial, sans-serif; color: #ffffff; text-decoration: none; padding: 12px 24px; border-radius: 4px; display: inline-block;">
                            {{ $slot }}
                        </a>
                    </td>
                </tr>
            </table>
        </td>
    </tr>
</table>
```

Usage in email templates:

```html
<!-- resources/views/emails/password-reset.blade.php -->
<x-email-layout>
    <h1>Password Reset Request</h1>
    <p>Hello {{ $user->name }},</p>
    <p>You requested a password reset for your account. Please click the button below to reset your password.</p>
    
    <x-email.button :url="$resetUrl" color="#e53e3e">
        Reset Password
    </x-email.button>
    
    <p>If you didn't request a password reset, you can safely ignore this email.</p>
</x-email-layout>
```

### Creating a Base Email Layout

```html
<!-- resources/views/layouts/email.blade.php -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>{{ config('app.name') }}</title>
    <style>
        /* Base styles */
        body {
            margin: 0;
            padding: 0;
            font-family: Arial, Helvetica, sans-serif;
            font-size: 16px;
            line-height: 1.6;
            color: #333333;
            background-color: #f8f8f8;
        }
        .container {
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            background-color: #ffffff;
        }
        .header {
            text-align: center;
            padding: 20px 0;
            border-bottom: 1px solid #eeeeee;
        }
        .content {
            padding: 20px 0;
        }
        .footer {
            text-align: center;
            padding: 20px 0;
            border-top: 1px solid #eeeeee;
            font-size: 14px;
            color: #999999;
        }
        /* Add more styles as needed */
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <img src="{{ $message->embed(public_path('images/logo.png')) }}" alt="{{ config('app.name') }}" height="60">
        </div>
        
        <div class="content">
            @yield('content')
        </div>
        
        <div class="footer">
            <p>&copy; {{ date('Y') }} {{ config('app.name') }}. All rights reserved.</p>
            <p>
                <a href="{{ url('/terms') }}">Terms of Service</a> | 
                <a href="{{ url('/privacy') }}">Privacy Policy</a> | 
                <a href="{{ url('/unsubscribe/' . $unsubscribeToken) }}">Unsubscribe</a>
            </p>
        </div>
    </div>
</body>
</html>
```

## Queue Configuration for Emails

### Queue Configuration

Update your `.env` file:

```
QUEUE_CONNECTION=database
```

### Creating the Jobs Table

```bash
php artisan queue:table
php artisan migrate
```

### Queuing Emails

```php
Mail::to($user->email)->queue(new WelcomeEmail($user));
```

Or with specific queue and delay:

```php
Mail::to($user->email)
    ->later(now()->addMinutes(10), new WelcomeEmail($user));

// Or with specific queue
Mail::to($user->email)
    ->queue((new WelcomeEmail($user))->onQueue('emails'));
```

### Processing the Queue

```bash
php artisan queue:work --queue=emails
```

Or as a background service:

```bash
php artisan queue:work --queue=high,default,emails --sleep=3 --tries=3 --daemon
```

## Email Tracking and Analytics

### Setting Up Tracking

```php
public function build()
{
    return $this->subject('Newsletter')
                ->view('emails.newsletter')
                ->withSwiftMessage(function ($message) {
                    $message->getHeaders()
                            ->addTextHeader('X-Mailgun-Track', 'yes')
                            ->addTextHeader('X-Mailgun-Track-Clicks', 'yes')
                            ->addTextHeader('X-Mailgun-Track-Opens', 'yes')
                            ->addTextHeader('X-Mailgun-Variables', json_encode([
                                'campaign_id' => $this->campaign->id,
                                'user_id' => $this->user->id,
                            ]));
                });
}
```

### Creating a Webhook Handler

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\EmailEvent;
use Illuminate\Support\Facades\Log;

class MailgunWebhookController extends Controller
{
    public function handleWebhook(Request $request)
    {
        // Verify webhook signature
        if (!$this->verifyWebhookSignature($request)) {
            Log::warning('Invalid Mailgun webhook signature');
            return response()->json(['error' => 'Invalid signature'], 401);
        }
        
        $event = $request->input('event-data');
        $eventType = $event['event'];
        $recipient = $event['recipient'];
        $messageId = $event['message']['headers']['message-id'];
        
        // Extract custom variables
        $variables = json_decode($event['user-variables'] ?? '{}', true);
        $campaignId = $variables['campaign_id'] ?? null;
        $userId = $variables['user_id'] ?? null;
        
        try {
            // Log the event
            EmailEvent::create([
                'message_id' => $messageId,
                'event_type' => $eventType,
                'recipient' => $recipient,
                'campaign_id' => $campaignId,
                'user_id' => $userId,
                'metadata' => json_encode($event),
            ]);
            
            // Process specific event types
            switch ($eventType) {
                case 'delivered':
                    $this->handleDelivered($messageId, $userId);
                    break;
                
                case 'opened':
                    $this->handleOpened($messageId, $userId);
                    break;
                
                case 'clicked':
                    $url = $event['url'] ?? null;
                    $this->handleClicked($messageId, $userId, $url);
                    break;
                
                case 'bounced':
                    $error = $event['severity'] . ': ' . ($event['error'] ?? 'Unknown error');
                    $this->handleBounced($messageId, $recipient, $error);
                    break;
                
                case 'complained':
                    $this->handleComplained($messageId, $userId, $recipient);
                    break;
                
                case 'unsubscribed':
                    $this->handleUnsubscribed($messageId, $userId, $recipient);
                    break;
            }
            
            return response()->json(['status' => 'success']);
        } catch (\Exception $e) {
            Log::error('Failed to process Mailgun webhook: ' . $e->getMessage());
            return response()->json(['error' => 'Failed to process webhook'], 500);
        }
    }
    
    private function verifyWebhookSignature(Request $request)
    {
        $signature = $request->input('signature');
        
        if (!$signature) {
            return false;
        }
        
        $timestamp = $signature['timestamp'] ?? '';
        $token = $signature['token'] ?? '';
        $signature = $signature['signature'] ?? '';
        
        $calculatedSignature = hash_hmac('sha256', $timestamp . $token, config('services.mailgun.webhook_signing_key'));
        
        return hash_equals($calculatedSignature, $signature);
    }
    
    private function handleDelivered($messageId, $userId)
    {
        Log::info("Email delivered: {$messageId} to user {$userId}");
        // Update delivery status in your system
    }
    
    private function handleOpened($messageId, $userId)
    {
        Log::info("Email opened: {$messageId} by user {$userId}");
        // Track open rate
    }
    
    private function handleClicked($messageId, $userId, $url)
    {
        Log::info("Email link clicked: {$messageId} by user {$userId}, URL: {$url}");
        // Track click rate and popular links
    }
    
    private function handleBounced($messageId, $recipient, $error)
    {
        Log::warning("Email bounced: {$messageId} to {$recipient}, Error: {$error}");
        // Flag email as invalid in your user database
    }
    
    private function handleComplained($messageId, $userId, $recipient)
    {
        Log::warning("Spam complaint: {$messageId} from {$recipient}");
        // Unsubscribe user from all marketing emails
    }
    
    private function handleUnsubscribed($messageId, $userId, $recipient)
    {
        Log::info("User unsubscribed: {$messageId}, {$recipient}");
        // Update user preferences
    }
}
```

### Registering the Webhook Route

```php
Route::post('mailgun/webhook', [\App\Http\Controllers\MailgunWebhookController::class, 'handleWebhook'])
    ->name('mailgun.webhook');
```

## Debugging and Testing

### Local Email Testing

Update your `.env` for local development:

```
MAIL_MAILER=log
```

This will write all emails to the Laravel log file instead of sending them.

### Email Preview in Browser

Create a route for previewing emails:

```php
// routes/web.php
Route::get('/email/preview/{type}', function ($type) {
    $user = \App\Models\User::first();
    
    switch ($type) {
        case 'welcome':
            return new \App\Mail\WelcomeEmail($user);
        
        case 'reset-password':
            return new \App\Mail\ResetPasswordEmail($user, 'fake-token');
        
        case 'order-confirmation':
            $order = \App\Models\Order::latest()->first();
            return new \App\Mail\OrderConfirmation($user, $order);
        
        default:
            abort(404);
    }
});
```

### Testing Emails in Feature Tests

```php
<?php

namespace Tests\Feature;

use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Support\Facades\Mail;
use Tests\TestCase;
use App\Mail\WelcomeEmail;
use App\Models\User;

class UserRegistrationTest extends TestCase
{
    use RefreshDatabase;

    /** @test */
    public function welcome_email_is_sent_after_registration()
    {
        Mail::fake();

        $userData = [
            'name' => 'Test User',
            'email' => 'test@example.com',
            'password' => 'password',
            'password_confirmation' => 'password'
        ];

        $response = $this->post('/register', $userData);

        $response->assertRedirect('/dashboard');
        Mail::assertSent(WelcomeEmail::class, function ($mail) use ($userData) {
            return $mail->hasTo($userData['email']) &&
                   $mail->user->name === $userData['name'];
        });
    }
}
```

## Integration with Filament

### Email Log Resource

```php
<?php

namespace App\Filament\Resources;

use App\Filament\Resources\EmailLogResource\Pages;
use App\Models\EmailEvent;
use Filament\Forms;
use Filament\Resources\Form;
use Filament\Resources\Resource;
use Filament\Resources\Table;
use Filament\Tables;

class EmailLogResource extends Resource
{
    protected static ?string $model = EmailEvent::class;
    protected static ?string $navigationIcon = 'heroicon-o-mail';
    protected static ?string $navigationGroup = 'Communication';
    protected static ?string $navigationLabel = 'Email Logs';

    public static function form(Form $form): Form
    {
        return $form
            ->schema([
                Forms\Components\TextInput::make('message_id')
                    ->label('Message ID')
                    ->disabled(),
                
                Forms\Components\TextInput::make('event_type')
                    ->label('Event Type')
                    ->disabled(),
                
                Forms\Components\TextInput::make('recipient')
                    ->label('Recipient')
                    ->disabled(),
                
                Forms\Components\TextInput::make('campaign_id')
                    ->label('Campaign ID')
                    ->disabled(),
                
                Forms\Components\TextInput::make('user_id')
                    ->label('User ID')
                    ->disabled(),
                
                Forms\Components\Textarea::make('metadata')
                    ->label('Metadata')
                    ->disabled()
                    ->columnSpan(2),
                
                Forms\Components\DateTimePicker::make('created_at')
                    ->label('Created At')
                    ->disabled(),
            ]);
    }

    public static function table(Table $table): Table
    {
        return $table
            ->columns([
                Tables\Columns\TextColumn::make('id')
                    ->label('ID')
                    ->sortable(),
                
                Tables\Columns\TextColumn::make('event_type')
                    ->label('Event Type')
                    ->sortable()
                    ->searchable(),
                
                Tables\Columns\TextColumn::make('recipient')
                    ->label('Recipient')
                    ->searchable(),
                
                Tables\Columns\TextColumn::make('campaign_id')
                    ->label('Campaign')
                    ->searchable(),
                
                Tables\Columns\TextColumn::make('user.name')
                    ->label('User')
                    ->searchable(),
                
                Tables\Columns\TextColumn::make('created_at')
                    ->label('Date')
                    ->dateTime()
                    ->sortable(),
            ])
            ->filters([
                Tables\Filters\SelectFilter::make('event_type')
                    ->options([
                        'delivered' => 'Delivered',
                        'opened' => 'Opened',
                        'clicked' => 'Clicked',
                        'bounced' => 'Bounced',
                        'complained' => 'Complained',
                        'unsubscribed' => 'Unsubscribed',
                    ]),
                
                Tables\Filters\Filter::make('created_at')
                    ->form([
                        Forms\Components\DatePicker::make('created_from')
                            ->label('From'),
                        Forms\Components\DatePicker::make('created_until')
                            ->label('Until'),
                    ])
                    ->query(function ($query, array $data) {
                        return $query
                            ->when(
                                $data['created_from'],
                                fn ($query, $date) => $query->whereDate('created_at', '>=', $date)
                            )
                            ->when(
                                $data['created_until'],
                                fn ($query, $date) => $query->whereDate('created_at', '<=', $date)
                            );
                    }),
            ])
            ->actions([
                Tables\Actions\ViewAction::make(),
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
            'index' => Pages\ListEmailLogs::route('/'),
            'view' => Pages\ViewEmailLog::route('/{record}'),
        ];
    }
}
```

### Email Template Management

```php
<?php

namespace App\Filament\Resources;

use App\Filament\Resources\EmailTemplateResource\Pages;
use App\Models\EmailTemplate;
use Filament\Forms;
use Filament\Resources\Form;
use Filament\Resources\Resource;
use Filament\Resources\Table;
use Filament\Tables;
use Illuminate\Support\HtmlString;

class EmailTemplateResource extends Resource
{
    protected static ?string $model = EmailTemplate::class;
    protected static ?string $navigationIcon = 'heroicon-o-template';
    protected static ?string $navigationGroup = 'Communication';

    public static function form(Form $form): Form
    {
        return $form
            ->schema([
                Forms\Components\Card::make()
                    ->schema([
                        Forms\Components\TextInput::make('name')
                            ->required()
                            ->maxLength(255),
                        
                        Forms\Components\TextInput::make('subject')
                            ->required()
                            ->maxLength(255),
                        
                        Forms\Components\Textarea::make('description')
                            ->rows(2)
                            ->maxLength(1000),
                        
                        Forms\Components\Select::make('type')
                            ->required()
                            ->options([
                                'transactional' => 'Transactional',
                                'marketing' => 'Marketing',
                                'notification' => 'Notification',
                            ]),
                        
                        Forms\Components\CodeEditor::make('content')
                            ->language('html')
                            ->required()
                            ->columnSpan(2),
                        
                        Forms\Components\Toggle::make('is_active')
                            ->label('Active')
                            ->default(true)
                            ->inline(false),
                        
                        Forms\Components\Section::make('Preview')
                            ->schema([
                                Forms\Components\View::make('filament.forms.components.html-preview')
                                    ->viewData([
                                        'content' => new HtmlString('{{ $record->content }}'),
                                    ]),
                            ])
                            ->columnSpan(2)
                            ->visible(fn ($livewire) => $livewire instanceof Pages\EditEmailTemplate),
                    ])
                    ->columns(2),
            ]);
    }

    public static function table(Table $table): Table
    {
        return $table
            ->columns([
                Tables\Columns\TextColumn::make('name')
                    ->searchable()
                    ->sortable(),
                
                Tables\Columns\TextColumn::make('subject')
                    ->searchable()
                    ->sortable(),
                
                Tables\Columns\BadgeColumn::make('type')
                    ->colors([
                        'primary' => 'transactional',
                        'success' => 'marketing',
                        'warning' => 'notification',
                    ]),
                
                Tables\Columns\IconColumn::make('is_active')
                    ->label('Active')
                    ->boolean(),
                
                Tables\Columns\TextColumn::make('updated_at')
                    ->label('Last Updated')
                    ->dateTime()
                    ->sortable(),
            ])
            ->filters([
                Tables\Filters\SelectFilter::make('type')
                    ->options([
                        'transactional' => 'Transactional',
                        'marketing' => 'Marketing',
                        'notification' => 'Notification',
                    ]),
                
                Tables\Filters\TernaryFilter::make('is_active')
                    ->label('Active Status')
                    ->placeholder('All Templates')
                    ->trueLabel('Active Templates')
                    ->falseLabel('Inactive Templates'),
            ])
            ->actions([
                Tables\Actions\Action::make('preview')
                    ->label('Preview')
                    ->icon('heroicon-o-eye')
                    ->url(fn (EmailTemplate $record) => route('email-templates.preview', $record))
                    ->openUrlInNewTab(),
                
                Tables\Actions\Action::make('duplicate')
                    ->label('Duplicate')
                    ->icon('heroicon-o-duplicate')
                    ->action(function (EmailTemplate $record) {
                        $newTemplate = $record->replicate();
                        $newTemplate->name = $record->name . ' (Copy)';
                        $newTemplate->is_active = false;
                        $newTemplate->save();
                    }),
                
                Tables\Actions\EditAction::make(),
                Tables\Actions\DeleteAction::make(),
            ])
            ->bulkActions([
                Tables\Actions\DeleteBulkAction::make(),
                Tables\Actions\BulkAction::make('activate')
                    ->label('Activate Selected')
                    ->icon('heroicon-o-check-circle')
                    ->action(fn ($records) => $records->each->update(['is_active' => true])),
                Tables\Actions\BulkAction::make('deactivate')
                    ->label('Deactivate Selected')
                    ->icon('heroicon-o-x-circle')
                    ->action(fn ($records) => $records->each->update(['is_active' => false])),
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
            'index' => Pages\ListEmailTemplates::route('/'),
            'create' => Pages\CreateEmailTemplate::route('/create'),
            'edit' => Pages\EditEmailTemplate::route('/{record}/edit'),
        ];
    }
}
``` 