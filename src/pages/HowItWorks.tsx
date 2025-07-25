import { Link } from 'react-router-dom';
import { Button } from '../components/ui/button';
import { Card, CardContent } from '../components/ui/card';
import { 
  Search, 
  Bell, 
  TrendingDown, 
  Mail, 
  DollarSign, 
  Plane,
  ArrowRight,
  Link as LinkIcon,
  Target,
  Clock,
  CheckCircle
} from 'lucide-react';

const HowItWorks = () => {
  const steps = [
    {
      icon: <LinkIcon className="h-6 w-6" />,
      title: "Copy Holiday URL",
      description: "Find your dream holiday on any major booking site and copy the URL.",
      color: "text-blue-500"
    },
    {
      icon: <Target className="h-6 w-6" />,
      title: "Set Target Price",
      description: "Tell us your desired price - we'll monitor it for you.",
      color: "text-green-500"
    },
    {
      icon: <Clock className="h-6 w-6" />,
      title: "We Monitor 24/7",
      description: "Our system checks prices every hour, day and night.",
      color: "text-purple-500"
    },
    {
      icon: <Bell className="h-6 w-6" />,
      title: "Get Notified",
      description: "Receive instant alerts when prices drop to your target.",
      color: "text-orange-500"
    },
    {
      icon: <CheckCircle className="h-6 w-6" />,
      title: "Book & Save",
      description: "Snatch your dream holiday at your perfect price!",
      color: "text-teal-500"
    }
  ];

  const features = [
    {
      icon: <Search className="h-8 w-8" />,
      title: "Smart Price Tracking",
      description: "Advanced algorithms monitor holiday prices across multiple booking sites.",
      color: "bg-gradient-ocean"
    },
    {
      icon: <Bell className="h-8 w-8" />,
      title: "Instant Alerts",
      description: "Get real-time notifications via email when prices match your target.",
      color: "bg-gradient-sunset"
    },
    {
      icon: <TrendingDown className="h-8 w-8" />,
      title: "Price History",
      description: "View historical price trends to make informed decisions.",
      color: "bg-gradient-success"
    },
    {
      icon: <Mail className="h-8 w-8" />,
      title: "Email Updates",
      description: "Weekly summaries of price changes and market trends.",
      color: "bg-gradient-sky"
    },
    {
      icon: <DollarSign className="h-8 w-8" />,
      title: "Guaranteed Savings",
      description: "Only book when prices meet your budget requirements.",
      color: "bg-gradient-destructive"
    },
    {
      icon: <Plane className="h-8 w-8" />,
      title: "Multiple Destinations",
      description: "Track up to 5 different holidays simultaneously.",
      color: "bg-gradient-ocean"
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-sky py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-16">
          <h1 className="text-4xl md:text-5xl font-bold text-foreground mb-4">
            How Trip Snatchers Works
          </h1>
          <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
            Track holiday prices effortlessly and never miss a deal again. Here's how our smart price tracking system helps you save money.
          </p>
        </div>

        {/* Steps */}
        <div className="relative mb-24">
          <div className="hidden md:block absolute top-1/2 left-0 right-0 h-0.5 bg-gradient-to-r from-primary/10 via-primary/20 to-primary/10 transform -translate-y-1/2" />
          <div className="grid grid-cols-1 md:grid-cols-5 gap-8">
            {steps.map((step, index) => (
              <div key={step.title} className="relative">
                <Card className="shadow-soft hover:shadow-glow transition-all duration-300">
                  <CardContent className="p-6 text-center">
                    <div className="inline-flex items-center justify-center w-12 h-12 rounded-full bg-gradient-ocean mb-4">
                      <div className={step.color}>{step.icon}</div>
                    </div>
                    <h3 className="text-lg font-semibold mb-2">{step.title}</h3>
                    <p className="text-muted-foreground">{step.description}</p>
                  </CardContent>
                </Card>
                {index < steps.length - 1 && (
                  <div className="hidden md:block absolute top-1/2 right-0 transform translate-x-1/2 -translate-y-1/2 z-10">
                    <ArrowRight className="h-6 w-6 text-primary/40" />
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Features */}
        <div className="mb-16">
          <h2 className="text-3xl font-bold text-center mb-12">
            Powerful Features for Smart Travelers
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature) => (
              <Card key={feature.title} className="shadow-soft hover:shadow-glow transition-all duration-300">
                <CardContent className="p-6">
                  <div className={`inline-flex items-center justify-center w-12 h-12 rounded-full ${feature.color} mb-4`}>
                    <div className="text-primary-foreground">{feature.icon}</div>
                  </div>
                  <h3 className="text-lg font-semibold mb-2">{feature.title}</h3>
                  <p className="text-muted-foreground">{feature.description}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>

        {/* CTA */}
        <div className="text-center">
          <Card className="bg-gradient-ocean border-none shadow-glow">
            <CardContent className="py-12">
              <h2 className="text-3xl font-bold text-primary-foreground mb-4">
                Ready to Start Saving?
              </h2>
              <p className="text-primary-foreground/90 mb-8 max-w-2xl mx-auto">
                Join thousands of smart travelers who are already saving money on their dream holidays.
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Button 
                  variant="secondary" 
                  size="lg"
                  asChild
                >
                  <Link to="/register">Start Tracking Now</Link>
                </Button>
                <Button 
                  variant="outline" 
                  size="lg"
                  className="bg-transparent border-primary-foreground text-primary-foreground hover:bg-primary-foreground/10"
                  asChild
                >
                  <Link to="/snatched-deals">View Recent Deals</Link>
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default HowItWorks; 