import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { Badge } from '../components/ui/badge';
import { useAuth } from '../context/AuthContext';
import { holidayApi, type HolidayTrack } from '../api/holidays';
import { toast } from '@/hooks/use-toast';
import { Plus, Trash2, ExternalLink, TrendingDown, TrendingUp, DollarSign, Calendar, MapPin, Bell } from 'lucide-react';

const Dashboard = () => {
  const { user } = useAuth();
  const [holidays, setHolidays] = useState<HolidayTrack[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    console.log('Dashboard mounted, user:', user);
    fetchHolidays();
  }, []);

  const fetchHolidays = async () => {
    try {
      console.log('Fetching holidays...');
      const response = await holidayApi.getAllTracked();
      console.log('Holidays response:', response);
      setHolidays(response);
    } catch (error: any) {
      console.error('Error fetching holidays:', error);
      const errorMessage = error.response?.data?.detail || "Please try refreshing the page.";
      setError(errorMessage);
      toast({
        title: "Failed to load holidays",
        description: errorMessage,
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  const deleteHoliday = async (id: number) => {
    try {
      await holidayApi.stopTracking(id);
      setHolidays(holidays.filter(h => h.id !== id));
      toast({
        title: "Holiday removed",
        description: "Holiday tracking has been stopped.",
      });
    } catch (error: any) {
      toast({
        title: "Failed to remove holiday",
        description: error.response?.data?.detail || "Please try again later.",
        variant: "destructive",
      });
    }
  };

  const getStatusBadge = (holiday: HolidayTrack) => {
    if (!holiday.is_active) {
      return <Badge variant="secondary" className="bg-gradient-success text-accent-foreground">Deal Snatched!</Badge>;
    }
    
    if (holiday.current_price <= holiday.target_price) {
      return <Badge variant="secondary" className="bg-gradient-success text-accent-foreground animate-pulse-glow">Target Reached!</Badge>;
    }
    
    return <Badge variant="outline">Active</Badge>;
  };

  const getPriceIndicator = (holiday: HolidayTrack) => {
    if (holiday.current_price <= holiday.target_price) {
      return <TrendingDown className="h-4 w-4 text-accent" />;
    }
    return <TrendingUp className="h-4 w-4 text-muted-foreground" />;
  };

  // Early return for error state
  if (error) {
    return (
      <div className="min-h-screen bg-gradient-sky flex items-center justify-center">
        <Card className="w-full max-w-md mx-4">
          <CardContent className="pt-6">
            <div className="text-center">
              <h2 className="text-lg font-semibold text-destructive mb-2">Error Loading Dashboard</h2>
              <p className="text-muted-foreground mb-4">{error}</p>
              <Button onClick={() => window.location.reload()} variant="outline">
                Try Again
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-sky flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-muted-foreground">Loading your holidays...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-sky py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl md:text-4xl font-bold text-foreground mb-2">
                Welcome back, {user ? `${user.first_name} ${user.last_name}` : 'Traveler'}! 👋
              </h1>
              <p className="text-xl text-muted-foreground">
                Track your holidays and never miss a deal again
              </p>
            </div>
            <Link to="/track">
              <Button variant="ocean" size="lg" className="hidden sm:flex">
                <Plus className="h-5 w-5" />
                Track New Holiday
              </Button>
            </Link>
          </div>

          {/* Mobile Track Button */}
          <div className="mt-4 sm:hidden">
            <Link to="/track">
              <Button variant="ocean" className="w-full">
                <Plus className="h-5 w-5" />
                Track New Holiday
              </Button>
            </Link>
          </div>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <Card className="shadow-soft">
            <CardContent className="pt-6">
              <div className="flex items-center space-x-3">
                <div className="p-2 bg-gradient-ocean rounded-lg">
                  <Bell className="h-6 w-6 text-primary-foreground" />
                </div>
                <div>
                  <p className="text-2xl font-bold text-foreground">
                    {holidays.filter(h => h.is_active).length}
                  </p>
                  <p className="text-sm text-muted-foreground">Active Tracks</p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="shadow-soft">
            <CardContent className="pt-6">
              <div className="flex items-center space-x-3">
                <div className="p-2 bg-gradient-success rounded-lg">
                  <TrendingDown className="h-6 w-6 text-accent-foreground" />
                </div>
                <div>
                  <p className="text-2xl font-bold text-foreground">
                    {holidays.filter(h => !h.is_active).length}
                  </p>
                  <p className="text-sm text-muted-foreground">Deals Snatched</p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="shadow-soft">
            <CardContent className="pt-6">
              <div className="flex items-center space-x-3">
                <div className="p-2 bg-gradient-sunset rounded-lg">
                  <DollarSign className="h-6 w-6 text-warning-foreground" />
                </div>
                <div>
                  <p className="text-2xl font-bold text-foreground">
                    €{holidays.filter(h => !h.is_active)
                              .reduce((sum, h) => sum + (h.current_price - h.target_price), 0).toFixed(2)}
                  </p>
                  <p className="text-sm text-muted-foreground">Total Saved</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Holidays List */}
        <Card className="shadow-soft">
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <MapPin className="h-5 w-5" />
              <span>Your Tracked Holidays</span>
            </CardTitle>
            <CardDescription>
              Monitor price changes and get notified when your target price is reached
            </CardDescription>
          </CardHeader>
          <CardContent>
            {holidays.length === 0 ? (
              <div className="text-center py-12">
                <Bell className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                <h3 className="text-lg font-semibold text-foreground mb-2">No holidays tracked yet</h3>
                <p className="text-muted-foreground mb-6">
                  Start tracking your first holiday to get price drop alerts
                </p>
                <Link to="/track">
                  <Button variant="ocean">
                    <Plus className="h-4 w-4" />
                    Track Your First Holiday
                  </Button>
                </Link>
              </div>
            ) : (
              <div className="space-y-4">
                {holidays.map((holiday) => (
                  <div
                    key={holiday.id}
                    className="border border-border rounded-lg p-4 hover:shadow-soft transition-all duration-300"
                  >
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="flex items-center space-x-3 mb-3">
                          <h3 className="font-semibold text-foreground">
                            {new URL(holiday.url).hostname}
                          </h3>
                          {getStatusBadge(holiday)}
                        </div>
                        
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-3">
                          <div>
                            <p className="text-sm text-muted-foreground">Target Price</p>
                            <p className="font-semibold text-foreground">€{holiday.target_price}</p>
                          </div>
                          <div>
                            <p className="text-sm text-muted-foreground">Current Price</p>
                            <div className="flex items-center space-x-1">
                              <p className={`font-semibold ${
                                holiday.current_price <= holiday.target_price 
                                  ? 'text-accent animate-price-drop' 
                                  : 'text-foreground'
                              }`}>
                                €{holiday.current_price}
                              </p>
                              {getPriceIndicator(holiday)}
                            </div>
                          </div>
                          <div>
                            <p className="text-sm text-muted-foreground">Created</p>
                            <div className="flex items-center space-x-1">
                              <Calendar className="h-3 w-3 text-muted-foreground" />
                              <p className="text-sm text-foreground">
                                {new Date(holiday.created_at).toLocaleDateString()}
                              </p>
                            </div>
                          </div>
                        </div>

                        <div className="flex items-center space-x-4 text-sm text-muted-foreground">
                          <a
                            href={holiday.url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="flex items-center space-x-1 hover:text-primary transition-colors duration-300"
                          >
                            <ExternalLink className="h-3 w-3" />
                            <span>View Original</span>
                          </a>
                        </div>
                      </div>

                      {holiday.is_active && (
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => deleteHoliday(holiday.id)}
                          className="text-destructive hover:text-destructive hover:bg-destructive/10"
                        >
                          <Trash2 className="h-4 w-4" />
                        </Button>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Dashboard;