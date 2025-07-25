import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { Badge } from '../components/ui/badge';
import { Shield, CheckCircle, AlertTriangle, Info, Scale, Lock } from 'lucide-react';

const Compliance = () => {
  return (
    <div className="min-h-screen bg-gradient-sky py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-ocean rounded-full mb-6 shadow-glow">
            <Shield className="h-8 w-8 text-primary-foreground" />
          </div>
          <h1 className="text-4xl md:text-5xl font-bold text-foreground mb-4">
            Compliance & Terms
          </h1>
          <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
            Understanding our legal compliance, data protection practices, and terms of service.
          </p>
        </div>

        {/* Compliance Overview */}
        <Card className="shadow-soft mb-8">
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <CheckCircle className="h-5 w-5 text-accent" />
              <span>Compliance Overview</span>
            </CardTitle>
            <CardDescription>
              Trip Snatchers is committed to operating within all applicable legal frameworks
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-4">
                <div className="flex items-start space-x-3">
                  <Badge variant="secondary" className="bg-gradient-success text-accent-foreground mt-1">
                    <CheckCircle className="h-3 w-3" />
                  </Badge>
                  <div>
                    <h3 className="font-semibold text-foreground">GDPR Compliant</h3>
                    <p className="text-sm text-muted-foreground">
                      Full compliance with European General Data Protection Regulation
                    </p>
                  </div>
                </div>

                <div className="flex items-start space-x-3">
                  <Badge variant="secondary" className="bg-gradient-success text-accent-foreground mt-1">
                    <CheckCircle className="h-3 w-3" />
                  </Badge>
                  <div>
                    <h3 className="font-semibold text-foreground">Data Encryption</h3>
                    <p className="text-sm text-muted-foreground">
                      All data is encrypted in transit and at rest using industry standards
                    </p>
                  </div>
                </div>

                <div className="flex items-start space-x-3">
                  <Badge variant="secondary" className="bg-gradient-success text-accent-foreground mt-1">
                    <CheckCircle className="h-3 w-3" />
                  </Badge>
                  <div>
                    <h3 className="font-semibold text-foreground">Fair Use Policy</h3>
                    <p className="text-sm text-muted-foreground">
                      Respectful scraping practices that don't harm travel websites
                    </p>
                  </div>
                </div>
              </div>

              <div className="space-y-4">
                <div className="flex items-start space-x-3">
                  <Badge variant="secondary" className="bg-gradient-success text-accent-foreground mt-1">
                    <CheckCircle className="h-3 w-3" />
                  </Badge>
                  <div>
                    <h3 className="font-semibold text-foreground">Terms Compliance</h3>
                    <p className="text-sm text-muted-foreground">
                      We respect all website terms of service and robots.txt files
                    </p>
                  </div>
                </div>

                <div className="flex items-start space-x-3">
                  <Badge variant="secondary" className="bg-gradient-success text-accent-foreground mt-1">
                    <CheckCircle className="h-3 w-3" />
                  </Badge>
                  <div>
                    <h3 className="font-semibold text-foreground">User Privacy</h3>
                    <p className="text-sm text-muted-foreground">
                      We never share your personal data or tracking preferences
                    </p>
                  </div>
                </div>

                <div className="flex items-start space-x-3">
                  <Badge variant="secondary" className="bg-gradient-success text-accent-foreground mt-1">
                    <CheckCircle className="h-3 w-3" />
                  </Badge>
                  <div>
                    <h3 className="font-semibold text-foreground">Transparent Operations</h3>
                    <p className="text-sm text-muted-foreground">
                      Clear disclosure of our monitoring and notification methods
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Legal Framework */}
        <Card className="shadow-soft mb-8">
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Scale className="h-5 w-5 text-primary" />
              <span>Legal Framework</span>
            </CardTitle>
            <CardDescription>
              How Trip Snatchers operates within legal boundaries
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            <div>
              <h3 className="font-semibold text-foreground mb-3 flex items-center space-x-2">
                <Info className="h-4 w-4 text-primary" />
                <span>Price Monitoring</span>
              </h3>
              <p className="text-muted-foreground mb-3">
                Our price monitoring service operates by checking publicly available prices on travel websites. 
                This practice is:
              </p>
              <ul className="list-disc list-inside space-y-1 text-sm text-muted-foreground ml-4">
                <li>Legal under fair use and public information access principles</li>
                <li>Non-invasive and respectful to website resources</li>
                <li>Compliant with robots.txt and rate limiting guidelines</li>
                <li>Transparent to users about data sources and methods</li>
              </ul>
            </div>

            <div>
              <h3 className="font-semibold text-foreground mb-3 flex items-center space-x-2">
                <Lock className="h-4 w-4 text-primary" />
                <span>Data Protection</span>
              </h3>
              <p className="text-muted-foreground mb-3">
                We take data protection seriously and implement comprehensive measures:
              </p>
              <ul className="list-disc list-inside space-y-1 text-sm text-muted-foreground ml-4">
                <li>End-to-end encryption for all user communications</li>
                <li>Minimal data collection - only what's necessary for the service</li>
                <li>Regular security audits and vulnerability assessments</li>
                <li>Right to data portability and deletion under GDPR</li>
                <li>No third-party data sharing without explicit consent</li>
              </ul>
            </div>
          </CardContent>
        </Card>

        {/* Terms of Service */}
        <Card className="shadow-soft mb-8">
          <CardHeader>
            <CardTitle>Terms of Service</CardTitle>
            <CardDescription>
              By using Trip Snatchers, you agree to these terms and conditions
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            <div>
              <h3 className="font-semibold text-foreground mb-3">1. Service Description</h3>
              <p className="text-muted-foreground text-sm">
                Trip Snatchers provides holiday price monitoring and notification services. We track publicly 
                available prices on travel websites and notify users when prices meet their specified criteria. 
                This service is provided "as is" without guarantees of price accuracy or availability.
              </p>
            </div>

            <div>
              <h3 className="font-semibold text-foreground mb-3">2. User Responsibilities</h3>
              <ul className="list-disc list-inside space-y-1 text-sm text-muted-foreground ml-4">
                <li>Provide accurate contact information for notifications</li>
                <li>Use the service only for personal, non-commercial purposes</li>
                <li>Not attempt to circumvent rate limiting or monitoring restrictions</li>
                <li>Respect the intellectual property of monitored websites</li>
                <li>Report any technical issues or suspicious activity promptly</li>
              </ul>
            </div>

            <div>
              <h3 className="font-semibold text-foreground mb-3">3. Limitations and Disclaimers</h3>
              <ul className="list-disc list-inside space-y-1 text-sm text-muted-foreground ml-4">
                <li>Price accuracy depends on third-party website data</li>
                <li>Monitoring frequency may vary based on website accessibility</li>
                <li>We are not responsible for booking failures or price changes after notification</li>
                <li>Service availability may be limited by technical or legal constraints</li>
                <li>No guarantee that tracked prices will reach target levels</li>
              </ul>
            </div>

            <div>
              <h3 className="font-semibold text-foreground mb-3">4. Privacy Policy</h3>
              <p className="text-muted-foreground text-sm">
                Your privacy is important to us. We collect only essential information needed to provide 
                our service, including email addresses for notifications and URLs for price tracking. 
                We do not sell, rent, or share your personal information with third parties except as 
                required by law or with your explicit consent.
              </p>
            </div>

            <div>
              <h3 className="font-semibold text-foreground mb-3">5. Account Termination</h3>
              <p className="text-muted-foreground text-sm">
                You may terminate your account at any time through your dashboard. We reserve the right 
                to suspend or terminate accounts that violate these terms or engage in abusive behavior. 
                Upon termination, all tracking activities will cease and personal data will be deleted 
                according to our retention policy.
              </p>
            </div>
          </CardContent>
        </Card>

        {/* Important Notice */}
        <Card className="bg-warning/10 border-warning/20">
          <CardContent className="pt-6">
            <div className="flex items-start space-x-3">
              <AlertTriangle className="h-5 w-5 text-warning mt-1" />
              <div>
                <h3 className="font-semibold text-foreground mb-2">Important Notice</h3>
                <p className="text-sm text-muted-foreground">
                  Trip Snatchers is an independent service and is not affiliated with any travel booking 
                  websites. We provide price monitoring as a convenience to users but cannot guarantee 
                  price accuracy, availability, or successful bookings. Always verify prices and terms 
                  directly with the booking website before making reservations.
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Contact Information */}
        <Card className="mt-8 shadow-soft">
          <CardContent className="pt-6">
            <div className="text-center">
              <h3 className="font-semibold text-foreground mb-3">Questions about Compliance?</h3>
              <p className="text-muted-foreground mb-4">
                If you have questions about our compliance practices, data handling, or terms of service, 
                please don't hesitate to contact us.
              </p>
              <div className="space-y-2 text-sm text-muted-foreground">
                <p>Email: compliance@tripsnatchers.com</p>
                <p>Data Protection Officer: privacy@tripsnatchers.com</p>
                <p>Last updated: January 2024</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Compliance;