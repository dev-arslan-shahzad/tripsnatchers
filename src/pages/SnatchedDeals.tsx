import { useState, useEffect } from 'react';
import { Card, CardContent } from '../components/ui/card';
import { Badge } from '../components/ui/badge';
import { Button } from '../components/ui/button';
import client from '../api/client';
import { MapPin, Calendar, DollarSign, ExternalLink, TrendingDown, Sparkles } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

interface SnatchedDeal {
  id: number;
  holiday_url: string;
  initial_price: number;
  target_price: number;
  snatched_price: number;
  date_tracked: string;
  date_snatched: string;
  user_id: number;
}

const SnatchedDeals = () => {
  const [deals, setDeals] = useState<SnatchedDeal[]>([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    fetchDeals();
  }, []);

  const fetchDeals = async () => {
    try {
      const response = await client.get('/snatched/all');
      setDeals(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Failed to fetch deals:', error);
      setLoading(false);
    }
  };

  const getSavingsPercentage = (target: number, snatched: number) => {
    return Math.round(((target - snatched) / target) * 100);
  };

  const getCategoryEmoji = (savings: number) => {
    if (savings >= 500) return '🌟';
    if (savings >= 300) return '✨';
    if (savings >= 200) return '💫';
    return '💰';
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-sky flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-muted-foreground">Loading snatched deals...</p>
        </div>
      </div>
    );
  }

  const totalSavings = deals.reduce((sum, deal) => sum + (deal.target_price - deal.snatched_price), 0);
  const averageSavings = deals.length > 0 
    ? Math.round(deals.reduce((sum, deal) => sum + getSavingsPercentage(deal.target_price, deal.snatched_price), 0) / deals.length)
    : 0;

  return (
    <div className="min-h-screen bg-gradient-sky py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-success rounded-full mb-6 shadow-deal">
            <TrendingDown className="h-8 w-8 text-accent-foreground" />
          </div>
          <h1 className="text-4xl md:text-5xl font-bold text-foreground mb-4">
            Snatched Deals 🎯
          </h1>
          <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
            See what our community has saved recently. These are real deals that were tracked 
            and snatched when prices dropped to target levels.
          </p>
        </div>

        {/* Stats Banner */}
        <div className="bg-gradient-ocean rounded-lg p-6 mb-12 shadow-glow">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-center">
            <div>
              <div className="text-3xl font-bold text-primary-foreground mb-1">
                {totalSavings.toLocaleString()}
              </div>
              <div className="text-primary-foreground/80">Total Community Savings</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-primary-foreground mb-1">
                {deals.length}
              </div>
              <div className="text-primary-foreground/80">Deals Snatched</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-primary-foreground mb-1">
                {averageSavings}%
              </div>
              <div className="text-primary-foreground/80">Average Savings</div>
            </div>
          </div>
        </div>

        {/* Deals Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {deals.map((deal) => {
            const savings = deal.target_price - deal.snatched_price;
            return (
              <Card 
                key={deal.id} 
                className="group hover:shadow-deal transition-all duration-300 hover:-translate-y-1 overflow-hidden"
              >
                <CardContent className="p-0">
                  {/* Header with Savings Badge */}
                  <div className="relative bg-gradient-sky p-6 pb-4">
                    <div className="flex items-center justify-between mb-4">
                      <div className="text-5xl">{getCategoryEmoji(savings)}</div>
                      <Badge className="bg-gradient-success text-accent-foreground shadow-deal">
                        <Sparkles className="h-3 w-3 mr-1" />
                        {getSavingsPercentage(deal.target_price, deal.snatched_price)}% OFF
                      </Badge>
                    </div>
                    
                    <h3 className="font-bold text-xl text-foreground mb-2 flex items-center">
                      <MapPin className="h-5 w-5 mr-2 text-primary" />
                      Holiday Deal
                    </h3>
                    
                    <p className="text-muted-foreground text-sm break-all">
                      {deal.holiday_url}
                    </p>
                  </div>

                  {/* Pricing Details */}
                  <div className="p-6">
                    <div className="space-y-3">
                      <div className="flex justify-between items-center">
                        <span className="text-muted-foreground">Target Price:</span>
                        <span className="text-muted-foreground font-semibold">
                          {deal.target_price.toLocaleString()}
                        </span>
                      </div>
                      
                      <div className="flex justify-between items-center">
                        <span className="text-muted-foreground">Snatched Price:</span>
                        <span className="font-bold text-2xl text-accent">
                          {deal.snatched_price.toLocaleString()}
                        </span>
                      </div>
                      
                      <div className="flex justify-between items-center py-2 px-3 bg-gradient-success rounded-lg">
                        <span className="text-accent-foreground font-medium">You Save:</span>
                        <div className="flex items-center space-x-1">
                          <span className="font-bold text-xl text-accent-foreground">
                            {savings.toLocaleString()}
                          </span>
                        </div>
                      </div>
                    </div>

                    {/* Footer */}
                    <div className="flex items-center justify-between mt-4 pt-4 border-t border-border">
                      <div className="flex items-center space-x-1 text-sm text-muted-foreground">
                        <Calendar className="h-3 w-3" />
                        <span>Snatched {new Date(deal.date_snatched).toLocaleDateString()}</span>
                      </div>
                      
                      <Button 
                        variant="ghost" 
                        size="sm" 
                        className="text-primary hover:text-primary-glow"
                        onClick={() => window.open(deal.holiday_url, '_blank')}
                      >
                        <ExternalLink className="h-3 w-3 mr-1" />
                        Visit
                      </Button>
                    </div>
                  </div>
                </CardContent>
              </Card>
            );
          })}
        </div>

        {/* Call to Action */}
        <div className="text-center mt-16">
          <Card className="bg-muted border-primary/20 max-w-2xl mx-auto">
            <CardContent className="pt-8 pb-8">
              <TrendingDown className="h-12 w-12 text-primary mx-auto mb-4" />
              <h3 className="text-2xl font-bold text-foreground mb-4">
                Want to Snatch Your Own Deals?
              </h3>
              <p className="text-muted-foreground mb-6">
                Join our community and start tracking your dream holidays. 
                Get notified when prices drop and snatch amazing deals like these.
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Button 
                  variant="ocean" 
                  size="lg"
                  onClick={() => navigate('/track')}
                >
                  Start Tracking Holidays
                </Button>
                <Button 
                  variant="outline" 
                  size="lg"
                  onClick={() => navigate('/how-it-works')}
                >
                  Learn How It Works
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default SnatchedDeals;