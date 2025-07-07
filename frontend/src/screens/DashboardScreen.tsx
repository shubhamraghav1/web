import React from 'react';
import {
  View,
  StyleSheet,
  ScrollView,
  RefreshControl,
} from 'react-native';
import {
  Card,
  Title,
  Paragraph,
  Button,
  Chip,
  Text,
  ProgressBar,
  Avatar,
  List,
} from 'react-native-paper';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';

export default function DashboardScreen() {
  const [refreshing, setRefreshing] = React.useState(false);

  const onRefresh = React.useCallback(() => {
    setRefreshing(true);
    setTimeout(() => setRefreshing(false), 2000);
  }, []);

  const upcomingRenewals = [
    { id: 1, type: 'Health Insurance', member: 'John Smith', daysLeft: 7, amount: '$450' },
    { id: 2, type: 'Auto Insurance', member: 'Family Coverage', daysLeft: 23, amount: '$320' },
    { id: 3, type: 'Life Insurance', member: 'Sarah Smith', daysLeft: 45, amount: '$180' },
  ];

  const policyStats = {
    total: 8,
    active: 7,
    expiringSoon: 2,
    totalCoverage: '$2.4M',
  };

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView
        contentContainerStyle={styles.scrollContent}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
        }
      >
        {/* Welcome Header */}
        <Card style={styles.welcomeCard}>
          <Card.Content>
            <View style={styles.welcomeHeader}>
              <View>
                <Title style={styles.welcomeTitle}>Good Morning, John! 👋</Title>
                <Paragraph style={styles.welcomeSubtitle}>
                  Your family's insurance is secure and up to date
                </Paragraph>
              </View>
              <Avatar.Icon size={50} icon="account" style={styles.avatar} />
            </View>
          </Card.Content>
        </Card>

        {/* Quick Stats */}
        <View style={styles.statsContainer}>
          <Card style={styles.statCard}>
            <Card.Content style={styles.statContent}>
              <Text style={styles.statNumber}>{policyStats.total}</Text>
              <Text style={styles.statLabel}>Total Policies</Text>
            </Card.Content>
          </Card>

          <Card style={styles.statCard}>
            <Card.Content style={styles.statContent}>
              <Text style={styles.statNumber}>{policyStats.active}</Text>
              <Text style={styles.statLabel}>Active</Text>
            </Card.Content>
          </Card>

          <Card style={styles.statCard}>
            <Card.Content style={styles.statContent}>
              <Text style={styles.statNumber}>{policyStats.totalCoverage}</Text>
              <Text style={styles.statLabel}>Coverage</Text>
            </Card.Content>
          </Card>
        </View>

        {/* Alerts */}
        <Card style={styles.alertCard}>
          <Card.Content>
            <View style={styles.alertHeader}>
              <Ionicons name="warning" size={24} color="#FDB813" />
              <Title style={styles.alertTitle}>Attention Required</Title>
            </View>
            <Paragraph style={styles.alertText}>
              2 policies are expiring within 30 days. Review renewal options now.
            </Paragraph>
            <Button mode="outlined" style={styles.alertButton}>
              View Details
            </Button>
          </Card.Content>
        </Card>

        {/* Upcoming Renewals */}
        <Card style={styles.renewalsCard}>
          <Card.Content>
            <Title style={styles.cardTitle}>Upcoming Renewals</Title>
            {upcomingRenewals.map((renewal) => (
              <List.Item
                key={renewal.id}
                title={renewal.type}
                description={`${renewal.member} • Premium: ${renewal.amount}`}
                left={(props) => (
                  <Avatar.Icon
                    {...props}
                    size={40}
                    icon="calendar"
                    style={{
                      backgroundColor: renewal.daysLeft <= 7 ? '#e74c3c' : '#2E8B57',
                    }}
                  />
                )}
                right={() => (
                  <View style={styles.renewalRight}>
                    <Chip
                      mode="outlined"
                      style={{
                        backgroundColor: renewal.daysLeft <= 7 ? '#ffebee' : '#e8f5e8',
                      }}
                    >
                      {renewal.daysLeft} days
                    </Chip>
                  </View>
                )}
                style={styles.renewalItem}
              />
            ))}
          </Card.Content>
        </Card>

        {/* Quick Actions */}
        <Card style={styles.actionsCard}>
          <Card.Content>
            <Title style={styles.cardTitle}>Quick Actions</Title>
            <View style={styles.actionsGrid}>
              <Button
                mode="contained"
                icon="plus"
                style={styles.actionButton}
                buttonColor="#2E8B57"
              >
                Add Policy
              </Button>
              <Button
                mode="outlined"
                icon="upload"
                style={styles.actionButton}
              >
                Upload Document
              </Button>
              <Button
                mode="outlined"
                icon="account-plus"
                style={styles.actionButton}
              >
                Add Family Member
              </Button>
              <Button
                mode="outlined"
                icon="file-search"
                style={styles.actionButton}
              >
                Find Policy
              </Button>
            </View>
          </Card.Content>
        </Card>

        {/* Coverage Overview */}
        <Card style={styles.coverageCard}>
          <Card.Content>
            <Title style={styles.cardTitle}>Coverage Overview</Title>
            <View style={styles.coverageItem}>
              <Text style={styles.coverageLabel}>Health Insurance</Text>
              <ProgressBar progress={0.85} color="#2E8B57" style={styles.progressBar} />
              <Text style={styles.coverageValue}>$500K / $600K</Text>
            </View>
            <View style={styles.coverageItem}>
              <Text style={styles.coverageLabel}>Life Insurance</Text>
              <ProgressBar progress={0.75} color="#2E8B57" style={styles.progressBar} />
              <Text style={styles.coverageValue}>$1.5M / $2M</Text>
            </View>
            <View style={styles.coverageItem}>
              <Text style={styles.coverageLabel}>Auto Insurance</Text>
              <ProgressBar progress={0.60} color="#FDB813" style={styles.progressBar} />
              <Text style={styles.coverageValue}>$200K / $350K</Text>
            </View>
          </Card.Content>
        </Card>
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
  welcomeCard: {
    marginBottom: 16,
    elevation: 2,
  },
  welcomeHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  welcomeTitle: {
    color: '#0A2A4E',
    fontSize: 20,
  },
  welcomeSubtitle: {
    color: '#666',
    marginTop: 4,
  },
  avatar: {
    backgroundColor: '#0A2A4E',
  },
  statsContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 16,
  },
  statCard: {
    flex: 1,
    marginHorizontal: 4,
    elevation: 2,
  },
  statContent: {
    alignItems: 'center',
    paddingVertical: 8,
  },
  statNumber: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#0A2A4E',
  },
  statLabel: {
    fontSize: 12,
    color: '#666',
    marginTop: 4,
  },
  alertCard: {
    marginBottom: 16,
    elevation: 2,
    backgroundColor: '#fff3cd',
  },
  alertHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 8,
  },
  alertTitle: {
    marginLeft: 8,
    color: '#856404',
    fontSize: 16,
  },
  alertText: {
    color: '#856404',
    marginBottom: 12,
  },
  alertButton: {
    borderColor: '#FDB813',
  },
  renewalsCard: {
    marginBottom: 16,
    elevation: 2,
  },
  cardTitle: {
    color: '#0A2A4E',
    marginBottom: 12,
  },
  renewalItem: {
    paddingVertical: 8,
  },
  renewalRight: {
    justifyContent: 'center',
  },
  actionsCard: {
    marginBottom: 16,
    elevation: 2,
  },
  actionsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
  },
  actionButton: {
    width: '48%',
    marginBottom: 8,
  },
  coverageCard: {
    marginBottom: 16,
    elevation: 2,
  },
  coverageItem: {
    marginBottom: 16,
  },
  coverageLabel: {
    fontSize: 14,
    color: '#0A2A4E',
    marginBottom: 4,
  },
  progressBar: {
    height: 8,
    borderRadius: 4,
    marginBottom: 4,
  },
  coverageValue: {
    fontSize: 12,
    color: '#666',
    textAlign: 'right',
  },
});