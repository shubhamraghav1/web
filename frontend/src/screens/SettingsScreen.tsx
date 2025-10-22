import React, { useState } from 'react';
import {
  View,
  StyleSheet,
  ScrollView,
  Alert,
} from 'react-native';
import {
  Card,
  Title,
  Paragraph,
  Button,
  Text,
  List,
  Switch,
  Divider,
  Avatar,
} from 'react-native-paper';
import { SafeAreaView } from 'react-native-safe-area-context';

export default function SettingsScreen() {
  const [notificationsEnabled, setNotificationsEnabled] = useState(true);
  const [biometricEnabled, setBiometricEnabled] = useState(false);
  const [autoBackup, setAutoBackup] = useState(true);
  const [darkMode, setDarkMode] = useState(false);

  const handleLogout = () => {
    Alert.alert(
      'Logout',
      'Are you sure you want to logout?',
      [
        { text: 'Cancel', style: 'cancel' },
        { text: 'Logout', style: 'destructive', onPress: () => {} },
      ]
    );
  };

  const handleDeleteAccount = () => {
    Alert.alert(
      'Delete Account',
      'This action cannot be undone. All your data will be permanently deleted.',
      [
        { text: 'Cancel', style: 'cancel' },
        { text: 'Delete', style: 'destructive', onPress: () => {} },
      ]
    );
  };

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView contentContainerStyle={styles.scrollContent}>
        {/* Profile Section */}
        <Card style={styles.profileCard}>
          <Card.Content>
            <View style={styles.profileHeader}>
              <Avatar.Icon
                size={80}
                icon="account"
                style={styles.avatar}
              />
              <View style={styles.profileInfo}>
                <Title style={styles.profileName}>John Smith</Title>
                <Paragraph style={styles.profileEmail}>john.smith@email.com</Paragraph>
                <Paragraph style={styles.profileMember}>Family Administrator</Paragraph>
              </View>
            </View>
            <Button
              mode="outlined"
              icon="pencil"
              style={styles.editProfileButton}
            >
              Edit Profile
            </Button>
          </Card.Content>
        </Card>

        {/* Notification Settings */}
        <Card style={styles.settingsCard}>
          <Card.Content>
            <Title style={styles.cardTitle}>Notifications</Title>
            <List.Item
              title="Push Notifications"
              description="Receive alerts for policy renewals and important updates"
              left={(props) => <List.Icon {...props} icon="bell" />}
              right={() => (
                <Switch
                  value={notificationsEnabled}
                  onValueChange={setNotificationsEnabled}
                />
              )}
            />
            <Divider />
            <List.Item
              title="Email Reminders"
              description="Get email notifications 30 and 7 days before renewal"
              left={(props) => <List.Icon {...props} icon="email" />}
              right={() => <Switch value={true} onValueChange={() => {}} />}
            />
            <Divider />
            <List.Item
              title="SMS Alerts"
              description="Receive text messages for urgent policy matters"
              left={(props) => <List.Icon {...props} icon="message-text" />}
              right={() => <Switch value={false} onValueChange={() => {}} />}
            />
          </Card.Content>
        </Card>

        {/* Security Settings */}
        <Card style={styles.settingsCard}>
          <Card.Content>
            <Title style={styles.cardTitle}>Security</Title>
            <List.Item
              title="Biometric Login"
              description="Use fingerprint or face recognition to login"
              left={(props) => <List.Icon {...props} icon="fingerprint" />}
              right={() => (
                <Switch
                  value={biometricEnabled}
                  onValueChange={setBiometricEnabled}
                />
              )}
            />
            <Divider />
            <List.Item
              title="Change Password"
              description="Update your account password"
              left={(props) => <List.Icon {...props} icon="lock" />}
              right={(props) => <List.Icon {...props} icon="chevron-right" />}
              onPress={() => {}}
            />
            <Divider />
            <List.Item
              title="Two-Factor Authentication"
              description="Add an extra layer of security"
              left={(props) => <List.Icon {...props} icon="shield-check" />}
              right={(props) => <List.Icon {...props} icon="chevron-right" />}
              onPress={() => {}}
            />
          </Card.Content>
        </Card>

        {/* Data & Privacy */}
        <Card style={styles.settingsCard}>
          <Card.Content>
            <Title style={styles.cardTitle}>Data & Privacy</Title>
            <List.Item
              title="Auto Backup"
              description="Automatically backup your data to cloud storage"
              left={(props) => <List.Icon {...props} icon="cloud-upload" />}
              right={() => (
                <Switch
                  value={autoBackup}
                  onValueChange={setAutoBackup}
                />
              )}
            />
            <Divider />
            <List.Item
              title="Export Data"
              description="Download all your family and policy data"
              left={(props) => <List.Icon {...props} icon="download" />}
              right={(props) => <List.Icon {...props} icon="chevron-right" />}
              onPress={() => {}}
            />
            <Divider />
            <List.Item
              title="Privacy Policy"
              description="Read our privacy policy and terms"
              left={(props) => <List.Icon {...props} icon="file-document" />}
              right={(props) => <List.Icon {...props} icon="chevron-right" />}
              onPress={() => {}}
            />
          </Card.Content>
        </Card>

        {/* App Settings */}
        <Card style={styles.settingsCard}>
          <Card.Content>
            <Title style={styles.cardTitle}>App Settings</Title>
            <List.Item
              title="Dark Mode"
              description="Switch to dark theme"
              left={(props) => <List.Icon {...props} icon="theme-light-dark" />}
              right={() => (
                <Switch
                  value={darkMode}
                  onValueChange={setDarkMode}
                />
              )}
            />
            <Divider />
            <List.Item
              title="Language"
              description="English (US)"
              left={(props) => <List.Icon {...props} icon="translate" />}
              right={(props) => <List.Icon {...props} icon="chevron-right" />}
              onPress={() => {}}
            />
            <Divider />
            <List.Item
              title="Currency"
              description="USD ($)"
              left={(props) => <List.Icon {...props} icon="currency-usd" />}
              right={(props) => <List.Icon {...props} icon="chevron-right" />}
              onPress={() => {}}
            />
          </Card.Content>
        </Card>

        {/* Support */}
        <Card style={styles.settingsCard}>
          <Card.Content>
            <Title style={styles.cardTitle}>Support</Title>
            <List.Item
              title="Help Center"
              description="Get help and find answers to common questions"
              left={(props) => <List.Icon {...props} icon="help-circle" />}
              right={(props) => <List.Icon {...props} icon="chevron-right" />}
              onPress={() => {}}
            />
            <Divider />
            <List.Item
              title="Contact Support"
              description="Reach out to our support team"
              left={(props) => <List.Icon {...props} icon="headset" />}
              right={(props) => <List.Icon {...props} icon="chevron-right" />}
              onPress={() => {}}
            />
            <Divider />
            <List.Item
              title="App Version"
              description="1.0.0 (Preview)"
              left={(props) => <List.Icon {...props} icon="information" />}
            />
          </Card.Content>
        </Card>

        {/* Account Actions */}
        <Card style={styles.actionsCard}>
          <Card.Content>
            <Title style={styles.cardTitle}>Account Actions</Title>
            <Button
              mode="outlined"
              icon="logout"
              style={styles.logoutButton}
              onPress={handleLogout}
            >
              Logout
            </Button>
            <Button
              mode="text"
              icon="delete"
              style={styles.deleteButton}
              textColor="#e74c3c"
              onPress={handleDeleteAccount}
            >
              Delete Account
            </Button>
          </Card.Content>
        </Card>

        {/* App Info */}
        <View style={styles.appInfo}>
          <Text style={styles.appInfoText}>InsurAssure AI v1.0.0</Text>
          <Text style={styles.appInfoText}>Made with ❤️ for your family's security</Text>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F8F9FA',
  },
  scrollContent: {
    padding: 16,
  },
  profileCard: {
    marginBottom: 16,
    elevation: 2,
  },
  profileHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 16,
  },
  avatar: {
    backgroundColor: '#0A2A4E',
  },
  profileInfo: {
    marginLeft: 16,
    flex: 1,
  },
  profileName: {
    fontSize: 24,
    color: '#0A2A4E',
    marginBottom: 4,
  },
  profileEmail: {
    fontSize: 16,
    color: '#666',
    marginBottom: 2,
  },
  profileMember: {
    fontSize: 14,
    color: '#2E8B57',
  },
  editProfileButton: {
    borderColor: '#0A2A4E',
  },
  settingsCard: {
    marginBottom: 16,
    elevation: 2,
  },
  cardTitle: {
    color: '#0A2A4E',
    marginBottom: 8,
  },
  actionsCard: {
    marginBottom: 16,
    elevation: 2,
  },
  logoutButton: {
    marginBottom: 12,
    borderColor: '#0A2A4E',
  },
  deleteButton: {
    marginBottom: 8,
  },
  appInfo: {
    alignItems: 'center',
    marginTop: 20,
    marginBottom: 40,
  },
  appInfoText: {
    color: '#666',
    fontSize: 12,
    marginBottom: 4,
  },
});