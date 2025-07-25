import { Link } from 'react-router-dom';
import { Button } from '../components/ui/button';
import { Card, CardContent } from '../components/ui/card';
import { Badge } from '../components/ui/badge';
import { ArrowRight, TrendingDown, Bell, DollarSign, MapPin, Calendar } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

const Home = () => {
  const { user } = useAuth();

  // Mock example deals
  const exampleDeals = [
    {
      id: 1,
      destination: "Bali, Indonesia",
      originalPrice: 1299,
      snatchedPrice: 799,
      savings: 500,
      snatchedDate: "2024-01-15",
      image: "🏝️"
    },
    {
      id: 2,
      destination: "Tokyo, Japan", 
      originalPrice: 1599,
      snatchedPrice: 999,
      savings: 600,
      snatchedDate: "2024-01-12",
      image: "🗾"
    },
    {
      id: 3,
      destination: "Paris, France",
      originalPrice: 899,
      snatchedPrice: 549,
      savings: 350,
      snatchedDate: "2024-01-10",
      image: "🗼"
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-sky">
      {/* Hero Section */}
      <section className="relative py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl mx-auto text-center">
          <div className="animate-slide-up">
            <h1 className="text-5xl md:text-7xl font-bold text-foreground mb-6 leading-tight">
              Never Overpay for{' '}
              <span className="bg-gradient-ocean bg-clip-text text-transparent">
                Holidays
              </span>{' '}
              Again
            </h1>
            <p className="text-xl md:text-2xl text-muted-foreground mb-8 max-w-3xl mx-auto">
              Track holiday prices, get instant alerts when they drop, and snatch the best deals 
              before they disappear. Your dream vacation is just a price drop away.
            </p>
          </div>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-12">
            {user ? (
              <Link to="/track">
                <Button variant="hero" className="animate-slide-up">
                  <Bell className="h-5 w-5" />
                  Track a Holiday
                  <ArrowRight className="h-5 w-5" />
                </Button>
              </Link>
            ) : (
              <>
                <Link to="/register">
                  <Button variant="hero" className="animate-slide-up">
                    Get Started Free
                    <ArrowRight className="h-5 w-5" />
                  </Button>
                </Link>
                <Link to="/snatched-deals">
                  <Button variant="outline" size="lg" className="animate-slide-up">
                    View Snatched Deals
                    <TrendingDown className="h-5 w-5" />
                  </Button>
                </Link>
              </>
            )}
          </div>

          {/* Stats */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-3xl mx-auto animate-slide-up">
            <div className="text-center">
              <div className="text-3xl font-bold text-accent">€2.4M+</div>
              <div className="text-muted-foreground">Total Savings</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-accent">15,000+</div>
              <div className="text-muted-foreground">Deals Snatched</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-accent">24hrs</div>
              <div className="text-muted-foreground">Avg Alert Time</div>
            </div>
          </div>
        </div>
      </section>

      {/* Recent Snatched Deals */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-background">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-foreground mb-4">
              Recent Snatched Deals
            </h2>
            <p className="text-xl text-muted-foreground">
              See what our community has saved recently
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
            {exampleDeals.map((deal) => (
              <Card key={deal.id} className="group hover:shadow-deal transition-all duration-300 hover:-translate-y-1">
                <CardContent className="p-6">
                  <div className="flex items-center justify-between mb-4">
                    <div className="text-4xl">{deal.image}</div>
                    <Badge variant="secondary" className="bg-gradient-success text-accent-foreground">
                      <DollarSign className="h-3 w-3" />
                      €{deal.savings} saved
                    </Badge>
                  </div>
                  
                  <h3 className="font-semibold text-foreground mb-2 flex items-center">
                    <MapPin className="h-4 w-4 mr-1 text-muted-foreground" />
                    {deal.destination}
                  </h3>
                  
                  <div className="space-y-2">
                    <div className="flex justify-between items-center">
                      <span className="text-muted-foreground">Original Price:</span>
                      <span className="line-through text-muted-foreground">€{deal.originalPrice}</span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-muted-foreground">Snatched at:</span>
                      <span className="font-bold text-accent animate-price-drop">€{deal.snatchedPrice}</span>
                    </div>
                    <div className="flex items-center text-sm text-muted-foreground mt-3">
                      <Calendar className="h-3 w-3 mr-1" />
                      Snatched on {new Date(deal.snatchedDate).toLocaleDateString()}
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>

          <div className="text-center">
            <Link to="/snatched-deals">
              <Button variant="ocean" size="lg">
                View All Snatched Deals
                <ArrowRight className="h-5 w-5" />
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-muted">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-foreground mb-4">
              How Trip Snatchers Works
            </h2>
            <p className="text-xl text-muted-foreground">
              Three simple steps to start saving on your holidays
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center group">
              <div className="bg-gradient-ocean w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-6 shadow-glow group-hover:shadow-lg transition-all duration-300">
                <span className="text-2xl font-bold text-primary-foreground">1</span>
              </div>
              <h3 className="text-xl font-semibold text-foreground mb-3">Track Your Holiday</h3>
              <p className="text-muted-foreground">
                Paste the URL of your dream holiday and set your target price. We'll monitor it 24/7.
              </p>
            </div>

            <div className="text-center group">
              <div className="bg-gradient-success w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-6 shadow-deal group-hover:shadow-lg transition-all duration-300">
                <span className="text-2xl font-bold text-accent-foreground">2</span>
              </div>
              <h3 className="text-xl font-semibold text-foreground mb-3">Get Instant Alerts</h3>
              <p className="text-muted-foreground">
                When the price drops to your target or below, we'll notify you immediately via email.
              </p>
            </div>

            <div className="text-center group">
              <div className="bg-gradient-sunset w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-6 shadow-lg group-hover:shadow-xl transition-all duration-300">
                <span className="text-2xl font-bold text-warning-foreground">3</span>
              </div>
              <h3 className="text-xl font-semibold text-foreground mb-3">Snatch the Deal</h3>
              <p className="text-muted-foreground">
                Book your holiday at the perfect price and save hundreds on your dream vacation.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      {!user && (
        <section className="py-20 px-4 sm:px-6 lg:px-8 bg-gradient-ocean">
          <div className="max-w-4xl mx-auto text-center">
            <h2 className="text-3xl md:text-4xl font-bold text-primary-foreground mb-6">
              Ready to Start Saving on Holidays?
            </h2>
            <p className="text-xl text-primary-foreground/80 mb-8">
              Join thousands of smart travelers who never overpay for holidays.
            </p>
            <Link to="/register">
              <Button variant="warning" size="lg" className="text-lg px-8 py-6">
                Start Tracking for Free
                <ArrowRight className="h-5 w-5" />
              </Button>
            </Link>
          </div>
        </section>
      )}
    </div>
  );
};

export default Home;