import React, { useState } from 'react';
import {
  View,
  StyleSheet,
  ScrollView,
  FlatList,
} from 'react-native';
import {
  Card,
  Title,
  Paragraph,
  Button,
  Chip,
  Text,
  FAB,
  Searchbar,
  Avatar,
  List,
  Menu,
  Divider,
} from 'react-native-paper';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';

interface Policy {
  id: string;
  type: string;
  provider: string;
  policyNumber: string;
  premium: string;
  coverage: string;
  renewalDate: string;
  status: 'active' | 'expiring' | 'expired';
  member: string;
}

export default function PoliciesScreen() {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedFilter, setSelectedFilter] = useState('all');
  const [menuVisible, setMenuVisible] = useState(false);

  const policies: Policy[] = [
    {
      id: '1',
      type: 'Health Insurance',
      provider: 'BlueCross BlueShield',
      policyNumber: 'HC-2024-001',
      premium: '$450/month',
      coverage: '$500K',
      renewalDate: '2024-12-15',
      status: 'expiring',
      member: 'John Smith',
    },
    {
      id: '2',
      type: 'Auto Insurance',
      provider: 'State Farm',
      policyNumber: 'AUTO-789456',
      premium: '$320/month',
      coverage: '$200K',
      renewalDate: '2024-11-30',
      status: 'active',
      member: 'Family Coverage',
    },
    {
      id: '3',
      type: 'Life Insurance',
      provider: 'MetLife',
      policyNumber: 'LIFE-456123',
      premium: '$180/month',
      coverage: '$1.5M',
      renewalDate: '2025-01-20',
      status: 'active',
      member: 'Sarah Smith',
    },
    {
      id: '4',
      type: 'Home Insurance',
      provider: 'Allstate',
      policyNumber: 'HOME-654321',
      premium: '$250/month',
      coverage: '$750K',
      renewalDate: '2024-10-05',
      status: 'active',
      member: 'Property Coverage',
    },
  ];

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active':
        return '#2E8B57';
      case 'expiring':
        return '#FDB813';
      case 'expired':
        return '#e74c3c';
      default:
        return '#666';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'active':
        return 'checkmark-circle';
      case 'expiring':
        return 'warning';
      case 'expired':
        return 'close-circle';
      default:
        return 'help-circle';
    }
  };

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'Health Insurance':
        return 'medical';
      case 'Auto Insurance':
        return 'car';
      case 'Life Insurance':
        return 'heart';
      case 'Home Insurance':
        return 'home';
      default:
        return 'document';
    }
  };

  const filteredPolicies = policies.filter(policy => {
    const matchesSearch = policy.type.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         policy.provider.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         policy.member.toLowerCase().includes(searchQuery.toLowerCase());
    
    const matchesFilter = selectedFilter === 'all' || policy.status === selectedFilter;
    
    return matchesSearch && matchesFilter;
  });

  const renderPolicyCard = ({ item }: { item: Policy }) => (
    <Card style={styles.policyCard} key={item.id}>
      <Card.Content>
        <View style={styles.policyHeader}>
          <View style={styles.policyTitle}>
            <Avatar.Icon
              size={40}
              icon={getTypeIcon(item.type)}
              style={{ backgroundColor: '#0A2A4E' }}
            />
            <View style={styles.titleText}>
              <Title style={styles.policyType}>{item.type}</Title>
              <Paragraph style={styles.provider}>{item.provider}</Paragraph>
            </View>
          </View>
          <Chip
            icon={getStatusIcon(item.status)}
            style={{
              backgroundColor: getStatusColor(item.status),
            }}
            textStyle={{ color: 'white' }}
          >
            {item.status.toUpperCase()}
          </Chip>
        </View>

        <View style={styles.policyDetails}>
          <View style={styles.detailRow}>
            <Text style={styles.detailLabel}>Policy Number:</Text>
            <Text style={styles.detailValue}>{item.policyNumber}</Text>
          </View>
          <View style={styles.detailRow}>
            <Text style={styles.detailLabel}>Coverage:</Text>
            <Text style={styles.detailValue}>{item.coverage}</Text>
          </View>
          <View style={styles.detailRow}>
            <Text style={styles.detailLabel}>Premium:</Text>
            <Text style={styles.detailValue}>{item.premium}</Text>
          </View>
          <View style={styles.detailRow}>
            <Text style={styles.detailLabel}>Renewal Date:</Text>
            <Text style={styles.detailValue}>{item.renewalDate}</Text>
          </View>
          <View style={styles.detailRow}>
            <Text style={styles.detailLabel}>Covered Member:</Text>
            <Text style={styles.detailValue}>{item.member}</Text>
          </View>
        </View>

        <View style={styles.policyActions}>
          <Button mode="outlined" style={styles.actionButton}>
            View Details
          </Button>
          <Button mode="text" style={styles.actionButton}>
            Documents
          </Button>
          <Button mode="text" style={styles.actionButton}>
            Renew
          </Button>
        </View>
      </Card.Content>
    </Card>
  );

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <Searchbar
          placeholder="Search policies..."
          onChangeText={setSearchQuery}
          value={searchQuery}
          style={styles.searchbar}
        />
        
        <View style={styles.filterContainer}>
          <Menu
            visible={menuVisible}
            onDismiss={() => setMenuVisible(false)}
            anchor={
              <Button
                mode="outlined"
                onPress={() => setMenuVisible(true)}
                icon="filter"
                style={styles.filterButton}
              >
                Filter: {selectedFilter}
              </Button>
            }
          >
            <Menu.Item onPress={() => { setSelectedFilter('all'); setMenuVisible(false); }} title="All Policies" />
            <Menu.Item onPress={() => { setSelectedFilter('active'); setMenuVisible(false); }} title="Active" />
            <Menu.Item onPress={() => { setSelectedFilter('expiring'); setMenuVisible(false); }} title="Expiring Soon" />
            <Menu.Item onPress={() => { setSelectedFilter('expired'); setMenuVisible(false); }} title="Expired" />
          </Menu>
        </View>
      </View>

      <FlatList
        data={filteredPolicies}
        renderItem={renderPolicyCard}
        keyExtractor={(item) => item.id}
        contentContainerStyle={styles.listContainer}
        showsVerticalScrollIndicator={false}
      />

      <FAB
        icon="plus"
        style={styles.fab}
        onPress={() => {}}
        label="Add Policy"
      />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F8F9FA',
  },
  header: {
    padding: 16,
    backgroundColor: '#FFFFFF',
    elevation: 2,
  },
  searchbar: {
    marginBottom: 12,
  },
  filterContainer: {
    flexDirection: 'row',
    justifyContent: 'flex-end',
  },
  filterButton: {
    borderColor: '#0A2A4E',
  },
  listContainer: {
    padding: 16,
  },
  policyCard: {
    marginBottom: 16,
    elevation: 3,
  },
  policyHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 16,
  },
  policyTitle: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  titleText: {
    marginLeft: 12,
  },
  policyType: {
    fontSize: 18,
    color: '#0A2A4E',
    marginBottom: 4,
  },
  provider: {
    fontSize: 14,
    color: '#666',
  },
  policyDetails: {
    marginBottom: 16,
  },
  detailRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 8,
  },
  detailLabel: {
    fontSize: 14,
    color: '#666',
    flex: 1,
  },
  detailValue: {
    fontSize: 14,
    color: '#0A2A4E',
    fontWeight: '500',
    flex: 1,
    textAlign: 'right',
  },
  policyActions: {
    flexDirection: 'row',
    justifyContent: 'space-around',
  },
  actionButton: {
    flex: 1,
    marginHorizontal: 4,
  },
  fab: {
    position: 'absolute',
    margin: 16,
    right: 0,
    bottom: 0,
    backgroundColor: '#2E8B57',
  },
});