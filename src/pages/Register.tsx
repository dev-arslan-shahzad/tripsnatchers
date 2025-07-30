import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select';
import { useAuth } from '../context/AuthContext';
import { toast } from '@/hooks/use-toast';
import { User, Mail, Phone, Lock, Globe, Plane, RefreshCw } from 'lucide-react';
import type { RegisterData } from '../api/auth';
import { authApi } from '../api/auth';

const Register = () => {
  const [formData, setFormData] = useState<RegisterData & { confirmPassword: string }>({
    first_name: '',
    last_name: '',
    email: '',
    phone: '',
    password: '',
    confirmPassword: '',
    country: '',
    date_of_birth: undefined,
    gender: undefined
  });
  const [loading, setLoading] = useState(false);
  const [showVerification, setShowVerification] = useState(false);
  const [resendLoading, setResendLoading] = useState(false);
  const { register } = useAuth();
  const navigate = useNavigate();

  const handleChange = (field: keyof (RegisterData & { confirmPassword: string }), value: string | number | undefined) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleResendVerification = async () => {
    setResendLoading(true);
    try {
      await authApi.resendVerification(formData.email);
      toast({
        title: "Verification email sent",
        description: "Please check your email for the verification link.",
      });
    } catch (error: any) {
      console.error('Resend verification error:', error);
      toast({
        title: "Failed to resend verification",
        description: error.response?.data?.detail || error.message || "Please try again later.",
        variant: "destructive",
      });
      // Don't hide the verification screen on error
    } finally {
      setResendLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (formData.password !== formData.confirmPassword) {
      toast({
        title: "Password mismatch",
        description: "Passwords do not match. Please try again.",
        variant: "destructive",
      });
      return;
    }

    // Split full name into first and last name
    const [firstName, ...lastNameParts] = formData.first_name.split(' ');
    const lastName = lastNameParts.join(' ');

    if (!lastName) {
      toast({
        title: "Invalid name",
        description: "Please enter both first and last name.",
        variant: "destructive",
      });
      return;
    }

    setLoading(true);

    try {
      const { confirmPassword, ...registrationData } = formData;
      const response = await authApi.register({
        ...registrationData,
        first_name: firstName,
        last_name: lastName
      });
      
      setShowVerification(true);
      toast({
        title: "Registration successful!",
        description: "Please check your email for the verification link.",
      });
    } catch (error: any) {
      const status = error.response?.status;
      const detail = error.response?.data?.detail;

      if (status === 202) {
        // User exists but not verified
        setShowVerification(true);
        toast({
          title: "Account exists",
          description: detail || "A new verification email has been sent.",
        });
      } else {
        toast({
          title: "Registration failed",
          description: detail || "Please try again later.",
          variant: "destructive",
        });
      }
    } finally {
      setLoading(false);
    }
  };

  if (showVerification) {
    return (
      <div className="min-h-screen bg-gradient-sky py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-md w-full mx-auto">
          <Card className="shadow-soft">
            <CardContent className="pt-6">
              <div className="text-center">
                <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-ocean rounded-full mb-4">
                  <Mail className="h-8 w-8 text-primary-foreground" />
                </div>
                <h2 className="text-2xl font-bold text-foreground mb-2">
                  Check Your Email
                </h2>
                <p className="text-muted-foreground mb-6">
                  We've sent a verification link to <strong>{formData.email}</strong>. 
                  Please check your email and click the link to verify your account.
                </p>
                <div className="space-y-4">
                  <Button
                    variant="outline"
                    className="w-full"
                    onClick={handleResendVerification}
                    disabled={resendLoading}
                  >
                    <RefreshCw className={`h-4 w-4 mr-2 ${resendLoading ? 'animate-spin' : ''}`} />
                    {resendLoading ? "Sending..." : "Resend Verification Email"}
                  </Button>
                  <Button
                    variant="ghost"
                    className="w-full"
                    onClick={() => navigate('/login')}
                  >
                    Go to Login
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-sky py-12 px-4 sm:px-6 lg:px-8">
      {/* Rest of the registration form JSX */}
      <div className="max-w-md w-full mx-auto space-y-8">
        {/* Header */}
        <div className="text-center">
          <Link to="/" className="inline-flex items-center space-x-2 group">
            <div className="p-3 bg-gradient-ocean rounded-lg shadow-glow group-hover:shadow-lg transition-all duration-300">
              <Plane className="h-8 w-8 text-primary-foreground" />
            </div>
            <span className="text-2xl font-bold bg-gradient-ocean bg-clip-text text-transparent">
              Trip Snatchers
            </span>
          </Link>
          <h2 className="mt-6 text-3xl font-bold text-foreground">
            Join Trip Snatchers
          </h2>
          <p className="mt-2 text-muted-foreground">
            Start saving on your dream holidays today
          </p>
        </div>

        {/* Registration Form */}
        <Card className="shadow-soft">
          <CardHeader>
            <CardTitle>Create Account</CardTitle>
            <CardDescription>
              Join thousands of smart travelers saving on holidays
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4">
              {/* Full Name */}
              <div className="space-y-2">
                <Label htmlFor="first_name">Full Name *</Label>
                <div className="relative">
                  <User className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                  <Input
                    id="first_name"
                    type="text"
                    placeholder="John Doe"
                    value={formData.first_name}
                    onChange={(e) => handleChange('first_name', e.target.value)}
                    className="pl-10"
                    required
                  />
                </div>
              </div>

              {/* Email */}
              <div className="space-y-2">
                <Label htmlFor="email">Email *</Label>
                <div className="relative">
                  <Mail className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                  <Input
                    id="email"
                    type="email"
                    placeholder="john@example.com"
                    value={formData.email}
                    onChange={(e) => handleChange('email', e.target.value)}
                    className="pl-10"
                    required
                  />
                </div>
              </div>

              {/* Phone */}
              <div className="space-y-2">
                <Label htmlFor="phone">Phone *</Label>
                <div className="relative">
                  <Phone className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                  <Input
                    id="phone"
                    type="tel"
                    placeholder="+1 234 567 8900"
                    value={formData.phone}
                    onChange={(e) => handleChange('phone', e.target.value)}
                    className="pl-10"
                    required
                  />
                </div>
              </div>

              {/* Password */}
              <div className="space-y-2">
                <Label htmlFor="password">Password *</Label>
                <div className="relative">
                  <Lock className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                  <Input
                    id="password"
                    type="password"
                    placeholder="Create a strong password"
                    value={formData.password}
                    onChange={(e) => handleChange('password', e.target.value)}
                    className="pl-10"
                    required
                  />
                </div>
              </div>

              {/* Confirm Password */}
              <div className="space-y-2">
                <Label htmlFor="confirmPassword">Confirm Password *</Label>
                <div className="relative">
                  <Lock className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                  <Input
                    id="confirmPassword"
                    type="password"
                    placeholder="Confirm your password"
                    value={formData.confirmPassword}
                    onChange={(e) => handleChange('confirmPassword', e.target.value)}
                    className="pl-10"
                    required
                  />
                </div>
              </div>

              {/* Country */}
              <div className="space-y-2">
                <Label htmlFor="country">Country *</Label>
                <div className="relative">
                  <Globe className="absolute left-3 top-3 h-4 w-4 text-muted-foreground z-10" />
                  <Select value={formData.country} onValueChange={(value) => handleChange('country', value)}>
                    <SelectTrigger className="pl-10">
                      <SelectValue placeholder="Select your country" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="us">United States</SelectItem>
                      <SelectItem value="uk">United Kingdom</SelectItem>
                      <SelectItem value="de">Germany</SelectItem>
                      <SelectItem value="fr">France</SelectItem>
                      <SelectItem value="es">Spain</SelectItem>
                      <SelectItem value="it">Italy</SelectItem>
                      <SelectItem value="nl">Netherlands</SelectItem>
                      <SelectItem value="ca">Canada</SelectItem>
                      <SelectItem value="au">Australia</SelectItem>
                      <SelectItem value="other">Other</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>

              {/* Optional Fields */}
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="date_of_birth">Date of Birth (Optional)</Label>
                  <Input
                    id="date_of_birth"
                    type="date"
                    value={formData.date_of_birth || ''}
                    onChange={(e) => handleChange('date_of_birth', e.target.value || undefined)}
                    max={new Date().toISOString().split('T')[0]}
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="gender">Gender (Optional)</Label>
                  <Select 
                    value={formData.gender || ''} 
                    onValueChange={(value) => handleChange('gender', value || undefined)}
                  >
                    <SelectTrigger>
                      <SelectValue placeholder="Select" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="male">Male</SelectItem>
                      <SelectItem value="female">Female</SelectItem>
                      <SelectItem value="other">Other</SelectItem>
                      <SelectItem value="prefer-not-to-say">Prefer not to say</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>

              <Button 
                type="submit" 
                variant="ocean" 
                className="w-full" 
                disabled={loading}
              >
                {loading ? "Creating account..." : "Create Account"}
              </Button>
            </form>

            <div className="mt-6 text-center">
              <p className="text-muted-foreground">
                Already have an account?{' '}
                <Link 
                  to="/login" 
                  className="text-primary hover:text-primary-glow transition-colors duration-300 font-medium"
                >
                  Sign in here
                </Link>
              </p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Register;