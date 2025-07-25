import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { Checkbox } from '../components/ui/checkbox';
import { toast } from '@/hooks/use-toast';
import { holidayApi } from '../api/holidays';
import { Link2, DollarSign, Bell, Info } from 'lucide-react';

interface TrackHolidayProps {
  initialPrice?: number;
}

const TrackHoliday = ({ initialPrice }: TrackHolidayProps) => {
  const [url, setUrl] = useState('');
  const [targetPrice, setTargetPrice] = useState('');
  const [complianceAccepted, setComplianceAccepted] = useState(false);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!complianceAccepted) {
      toast({
        title: "Compliance required",
        description: "Please accept the compliance terms to continue.",
        variant: "destructive",
      });
      return;
    }

    setLoading(true);

    try {
      await holidayApi.startTracking({
        url,
        target_price: parseFloat(targetPrice),
      });

      toast({
        title: "Holiday tracked successfully!",
        description: "We'll notify you when the price drops to your target.",
      });

      navigate('/dashboard');
    } catch (error: any) {
      toast({
        title: "Failed to track holiday",
        description: error.response?.data?.detail || "Please try again later.",
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-sky py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-2xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-ocean rounded-full mb-4 shadow-glow">
            <Bell className="h-8 w-8 text-primary-foreground" />
          </div>
          <h1 className="text-3xl md:text-4xl font-bold text-foreground mb-4">
            Track Your Dream Holiday
          </h1>
          <p className="text-xl text-muted-foreground">
            Set up price monitoring and get notified when your target price is reached
          </p>
        </div>

        {/* Main Form */}
        <Card className="shadow-soft mb-6">
          <CardHeader>
            <CardTitle>Holiday Details</CardTitle>
            <CardDescription>
              Enter the holiday URL and your target price to start tracking
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-6">
              <div className="space-y-2">
                <Label htmlFor="url">Holiday URL</Label>
                <div className="relative">
                  <Link2 className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                  <Input
                    id="url"
                    type="url"
                    placeholder="https://example.com/holiday-package"
                    value={url}
                    onChange={(e) => setUrl(e.target.value)}
                    className="pl-10"
                    required
                  />
                </div>
                <p className="text-sm text-muted-foreground">
                  Copy and paste the URL from booking sites like Booking.com, Expedia, etc.
                </p>
              </div>

              <div className="space-y-2">
                <Label htmlFor="targetPrice">Target Price (€)</Label>
                <div className="relative">
                  <DollarSign className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                  <Input
                    id="targetPrice"
                    type="number"
                    placeholder="999"
                    value={targetPrice}
                    onChange={(e) => setTargetPrice(e.target.value)}
                    className="pl-10"
                    min="0"
                    step="0.01"
                    required
                  />
                </div>
                <p className="text-sm text-muted-foreground">
                  We'll alert you when the price drops to this amount or below
                </p>
              </div>

              {initialPrice && (
                <div className="p-4 bg-muted rounded-lg">
                  <p className="text-sm font-medium">Current Price: €{initialPrice}</p>
                  <p className="text-xs text-muted-foreground mt-1">
                    This price was fetched from your scraping script
                  </p>
                </div>
              )}

              <div className="flex items-start space-x-2">
                <Checkbox
                  id="compliance"
                  checked={complianceAccepted}
                  onCheckedChange={(checked) => setComplianceAccepted(checked === true)}
                />
                <div className="space-y-1 leading-none">
                  <Label htmlFor="compliance" className="text-sm font-normal">
                    I agree to the{' '}
                    <a 
                      href="/compliance" 
                      className="text-primary hover:text-primary-glow transition-colors duration-300 underline"
                      target="_blank"
                      rel="noopener noreferrer"
                    >
                      compliance terms and conditions
                    </a>
                  </Label>
                </div>
              </div>

              <Button 
                type="submit" 
                variant="ocean" 
                size="lg" 
                className="w-full" 
                disabled={loading || !complianceAccepted}
              >
                {loading ? "Setting up tracking..." : "Start Tracking"}
              </Button>
            </form>
          </CardContent>
        </Card>

        {/* Info Card */}
        <Card className="bg-muted border-primary/20">
          <CardContent className="pt-6">
            <div className="flex items-start space-x-3">
              <Info className="h-5 w-5 text-primary mt-0.5" />
              <div className="space-y-2">
                <h3 className="font-semibold text-foreground">How it works</h3>
                <ul className="text-sm text-muted-foreground space-y-1">
                  <li>• We check your holiday price every hour</li>
                  <li>• You'll get email alerts when prices drop</li>
                  <li>• Track up to 5 holidays on the free plan</li>
                  <li>• Cancel tracking anytime from your dashboard</li>
                </ul>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default TrackHoliday;