import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Button } from './ui/button';
import { Plane, User, LogOut, TrendingDown } from 'lucide-react';

const Navbar = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <nav className="bg-card border-b border-border shadow-soft">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-2 group">
            <div className="p-2 bg-gradient-ocean rounded-lg shadow-glow group-hover:shadow-lg transition-all duration-300">
              <Plane className="h-6 w-6 text-primary-foreground" />
            </div>
            <span className="text-xl font-bold bg-gradient-ocean bg-clip-text text-transparent">
              Trip Snatchers
            </span>
          </Link>

          {/* Navigation Links */}
          <div className="hidden md:flex items-center space-x-6">
            <Link 
              to="/snatched-deals" 
              className="flex items-center space-x-1 text-foreground hover:text-primary transition-colors duration-300"
            >
              <TrendingDown className="h-4 w-4" />
              <span>Snatched Deals</span>
            </Link>
            
            {user ? (
              <>
                <Link 
                  to="/dashboard" 
                  className="text-foreground hover:text-primary transition-colors duration-300"
                >
                  Dashboard
                </Link>
                <Link 
                  to="/track" 
                  className="text-foreground hover:text-primary transition-colors duration-300"
                >
                  Track Holiday
                </Link>
                <div className="flex items-center space-x-3">
                  <Link to="/profile">
                    <Button variant="ghost" size="sm">
                      <User className="h-4 w-4" />
                      Profile
                    </Button>
                  </Link>
                  <Button variant="outline" size="sm" onClick={handleLogout}>
                    <LogOut className="h-4 w-4" />
                    Logout
                  </Button>
                </div>
              </>
            ) : (
              <div className="flex items-center space-x-3">
                <Link to="/login">
                  <Button variant="ghost">Login</Button>
                </Link>
                <Link to="/register">
                  <Button variant="ocean">Get Started</Button>
                </Link>
              </div>
            )}
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden">
            {user ? (
              <Link to="/dashboard">
                <Button variant="ghost" size="sm">
                  <User className="h-4 w-4" />
                </Button>
              </Link>
            ) : (
              <Link to="/login">
                <Button variant="ocean" size="sm">Login</Button>
              </Link>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;