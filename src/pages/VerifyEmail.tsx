import { useEffect, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { Card, CardContent } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Mail, CheckCircle, XCircle } from 'lucide-react';
import { authApi } from '../api/auth';
import { toast } from '@/hooks/use-toast';

const VerifyEmail = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const [verifying, setVerifying] = useState(true);
  const [verified, setVerified] = useState(false);

  useEffect(() => {
    const token = searchParams.get('token');
    if (!token) {
      setVerifying(false);
      return;
    }

    verifyEmail(token);
  }, [searchParams]);

  const verifyEmail = async (token: string) => {
    try {
      await authApi.verifyEmail(token);
      setVerified(true);
      toast({
        title: "Email verified successfully!",
        description: "You can now log in to your account.",
      });
    } catch (error: any) {
      toast({
        title: "Verification failed",
        description: error.message || "Please try again or contact support.",
        variant: "destructive",
      });
    } finally {
      setVerifying(false);
    }
  };

  if (verifying) {
    return (
      <div className="min-h-screen bg-gradient-sky flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-muted-foreground">Verifying your email...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-sky py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md mx-auto">
        <Card className="shadow-soft">
          <CardContent className="pt-6">
            <div className="text-center">
              {verified ? (
                <>
                  <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-success rounded-full mb-4">
                    <CheckCircle className="h-8 w-8 text-accent-foreground" />
                  </div>
                  <h2 className="text-2xl font-bold text-foreground mb-2">
                    Email Verified!
                  </h2>
                  <p className="text-muted-foreground mb-6">
                    Your email has been verified successfully. You can now log in to your account.
                  </p>
                  <Button
                    variant="ocean"
                    className="w-full"
                    onClick={() => navigate('/login')}
                  >
                    Log In
                  </Button>
                </>
              ) : (
                <>
                  <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-destructive rounded-full mb-4">
                    <XCircle className="h-8 w-8 text-destructive-foreground" />
                  </div>
                  <h2 className="text-2xl font-bold text-foreground mb-2">
                    Verification Failed
                  </h2>
                  <p className="text-muted-foreground mb-6">
                    The verification link is invalid or has expired. Please try registering again
                    or contact support if you need help.
                  </p>
                  <div className="space-y-3">
                    <Button
                      variant="ocean"
                      className="w-full"
                      onClick={() => navigate('/register')}
                    >
                      Register Again
                    </Button>
                    <Button
                      variant="outline"
                      className="w-full"
                      onClick={() => navigate('/')}
                    >
                      Go Home
                    </Button>
                  </div>
                </>
              )}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default VerifyEmail; 