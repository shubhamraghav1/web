import React, { useState } from 'react';
import {
  View,
  StyleSheet,
  KeyboardAvoidingView,
  Platform,
  ScrollView,
  Image,
} from 'react-native';
import {
  TextInput,
  Button,
  Text,
  Card,
  Title,
  Paragraph,
  HelperText,
} from 'react-native-paper';
import { SafeAreaView } from 'react-native-safe-area-context';

interface LoginScreenProps {
  onLogin: () => void;
}

export default function LoginScreen({ onLogin }: LoginScreenProps) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);

  const handleLogin = async () => {
    setLoading(true);
    // Simulate API call
    setTimeout(() => {
      setLoading(false);
      onLogin();
    }, 1500);
  };

  const isValidEmail = (email: string) => {
    return /\S+@\S+\.\S+/.test(email);
  };

  return (
    <SafeAreaView style={styles.container}>
      <KeyboardAvoidingView
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
        style={styles.container}
      >
        <ScrollView contentContainerStyle={styles.scrollContent}>
          <View style={styles.header}>
            <View style={styles.logoContainer}>
              <Text style={styles.logoText}>🛡️</Text>
              <Title style={styles.appTitle}>InsurAssure AI</Title>
              <Paragraph style={styles.subtitle}>
                Your Family's Insurance Guardian
              </Paragraph>
            </View>
          </View>

          <Card style={styles.card}>
            <Card.Content>
              <Title style={styles.cardTitle}>Welcome Back</Title>
              <Paragraph style={styles.cardDescription}>
                Sign in to access your family's insurance vault
              </Paragraph>

              <TextInput
                label="Email Address"
                value={email}
                onChangeText={setEmail}
                mode="outlined"
                keyboardType="email-address"
                autoCapitalize="none"
                style={styles.input}
                left={<TextInput.Icon icon="email" />}
              />
              <HelperText type="error" visible={email.length > 0 && !isValidEmail(email)}>
                Please enter a valid email address
              </HelperText>

              <TextInput
                label="Password"
                value={password}
                onChangeText={setPassword}
                mode="outlined"
                secureTextEntry={!showPassword}
                style={styles.input}
                left={<TextInput.Icon icon="lock" />}
                right={
                  <TextInput.Icon
                    icon={showPassword ? 'eye-off' : 'eye'}
                    onPress={() => setShowPassword(!showPassword)}
                  />
                }
              />

              <Button
                mode="contained"
                onPress={handleLogin}
                loading={loading}
                disabled={!email || !password || !isValidEmail(email)}
                style={styles.loginButton}
                contentStyle={styles.buttonContent}
              >
                {loading ? 'Signing In...' : 'Sign In'}
              </Button>

              <View style={styles.footer}>
                <Button mode="text" onPress={() => {}}>
                  Forgot Password?
                </Button>
                <Button mode="text" onPress={() => {}}>
                  Create Account
                </Button>
              </View>
            </Card.Content>
          </Card>

          <View style={styles.demoNote}>
            <Text style={styles.demoText}>
              📱 Demo Mode: Click "Sign In" to preview the app
            </Text>
          </View>
        </ScrollView>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F8F9FA',
  },
  scrollContent: {
    flexGrow: 1,
    justifyContent: 'center',
    padding: 20,
  },
  header: {
    alignItems: 'center',
    marginBottom: 30,
  },
  logoContainer: {
    alignItems: 'center',
  },
  logoText: {
    fontSize: 48,
    marginBottom: 10,
  },
  appTitle: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#0A2A4E',
    marginBottom: 5,
  },
  subtitle: {
    fontSize: 16,
    color: '#2E8B57',
    textAlign: 'center',
  },
  card: {
    marginVertical: 20,
    elevation: 4,
  },
  cardTitle: {
    textAlign: 'center',
    color: '#0A2A4E',
    marginBottom: 10,
  },
  cardDescription: {
    textAlign: 'center',
    marginBottom: 20,
    color: '#666',
  },
  input: {
    marginBottom: 5,
  },
  loginButton: {
    marginTop: 20,
    marginBottom: 15,
    backgroundColor: '#0A2A4E',
  },
  buttonContent: {
    paddingVertical: 8,
  },
  footer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginTop: 10,
  },
  demoNote: {
    marginTop: 20,
    padding: 15,
    backgroundColor: '#FDB813',
    borderRadius: 8,
    alignItems: 'center',
  },
  demoText: {
    color: '#0A2A4E',
    fontWeight: '600',
    textAlign: 'center',
  },
});