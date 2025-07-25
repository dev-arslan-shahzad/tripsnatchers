import { Link } from 'react-router-dom';
import { Plane, Mail, Shield, FileText } from 'lucide-react';

const Footer = () => {
  return (
    <footer className="bg-muted border-t border-border">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Brand */}
          <div className="col-span-1 md:col-span-2">
            <div className="flex items-center space-x-2 mb-4">
              <div className="p-2 bg-gradient-ocean rounded-lg shadow-glow">
                <Plane className="h-6 w-6 text-primary-foreground" />
              </div>
              <span className="text-xl font-bold bg-gradient-ocean bg-clip-text text-transparent">
                Trip Snatchers
              </span>
            </div>
            <p className="text-muted-foreground max-w-md">
              Never overpay for holidays again. Track prices, get alerts, and snatch the best deals 
              when they drop. Your dream vacation is just a price drop away.
            </p>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="font-semibold text-foreground mb-4">Quick Links</h3>
            <ul className="space-y-2">
              <li>
                <Link to="/snatched-deals" className="text-muted-foreground hover:text-primary transition-colors duration-300">
                  Snatched Deals
                </Link>
              </li>
              <li>
                <Link to="/track" className="text-muted-foreground hover:text-primary transition-colors duration-300">
                  Track Holiday
                </Link>
              </li>
              <li>
                <Link to="/dashboard" className="text-muted-foreground hover:text-primary transition-colors duration-300">
                  Dashboard
                </Link>
              </li>
            </ul>
          </div>

          {/* Support */}
          <div>
            <h3 className="font-semibold text-foreground mb-4">Support</h3>
            <ul className="space-y-2">
              <li>
                <Link to="/compliance" className="text-muted-foreground hover:text-primary transition-colors duration-300 flex items-center space-x-1">
                  <Shield className="h-4 w-4" />
                  <span>Compliance</span>
                </Link>
              </li>
              <li>
                <a href="mailto:support@tripsnatchers.com" className="text-muted-foreground hover:text-primary transition-colors duration-300 flex items-center space-x-1">
                  <Mail className="h-4 w-4" />
                  <span>Contact</span>
                </a>
              </li>
              <li>
                <Link to="/terms" className="text-muted-foreground hover:text-primary transition-colors duration-300 flex items-center space-x-1">
                  <FileText className="h-4 w-4" />
                  <span>Terms</span>
                </Link>
              </li>
            </ul>
          </div>
        </div>

        <div className="border-t border-border mt-8 pt-8 text-center text-muted-foreground">
          <p>&copy; {new Date().getFullYear()} Trip Snatchers. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;