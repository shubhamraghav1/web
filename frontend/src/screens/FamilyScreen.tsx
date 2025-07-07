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
  Avatar,
  List,
  IconButton,
} from 'react-native-paper';
import { SafeAreaView } from 'react-native-safe-area-context';

interface FamilyMember {
  id: string;
  name: string;
  relationship: string;
  age: number;
  email: string;
  phone: string;
  policiesCount: number;
  avatar?: string;
}

export default function FamilyScreen() {
  const [familyMembers] = useState<FamilyMember[]>([
    {
      id: '1',
      name: 'John Smith',
      relationship: 'Self',
      age: 42,
      email: 'john.smith@email.com',
      phone: '+1 (555) 123-4567',
      policiesCount: 4,
    },
    {
      id: '2',
      name: 'Sarah Smith',
      relationship: 'Spouse',
      age: 38,
      email: 'sarah.smith@email.com',
      phone: '+1 (555) 123-4568',
      policiesCount: 3,
    },
    {
      id: '3',
      name: 'Emma Smith',
      relationship: 'Daughter',
      age: 16,
      email: 'emma.smith@email.com',
      phone: '+1 (555) 123-4569',
      policiesCount: 2,
    },
    {
      id: '4',
      name: 'Michael Smith',
      relationship: 'Son',
      age: 12,
      email: '',
      phone: '',
      policiesCount: 1,
    },
  ]);

  const getRelationshipColor = (relationship: string) => {
    switch (relationship.toLowerCase()) {
      case 'self':
        return '#0A2A4E';
      case 'spouse':
        return '#2E8B57';
      case 'daughter':
      case 'son':
        return '#FDB813';
      default:
        return '#666';
    }
  };

  const getAvatarIcon = (relationship: string) => {
    switch (relationship.toLowerCase()) {
      case 'self':
        return 'account';
      case 'spouse':
        return 'account-heart';
      case 'daughter':
        return 'account-child';
      case 'son':
        return 'account-child';
      default:
        return 'account-group';
    }
  };

  const renderFamilyMember = ({ item }: { item: FamilyMember }) => (
    <Card style={styles.memberCard} key={item.id}>
      <Card.Content>
        <View style={styles.memberHeader}>
          <View style={styles.memberInfo}>
            <Avatar.Icon
              size={60}
              icon={getAvatarIcon(item.relationship)}
              style={{
                backgroundColor: getRelationshipColor(item.relationship),
              }}
            />
            <View style={styles.memberDetails}>
              <Title style={styles.memberName}>{item.name}</Title>
              <View style={styles.relationshipContainer}>
                <Chip
                  mode="outlined"
                  style={{
                    borderColor: getRelationshipColor(item.relationship),
                  }}
                  textStyle={{
                    color: getRelationshipColor(item.relationship),
                  }}
                >
                  {item.relationship}
                </Chip>
                <Text style={styles.ageText}>Age {item.age}</Text>
              </View>
            </View>
          </View>
          <IconButton
            icon="dots-vertical"
            onPress={() => {}}
          />
        </View>

        <View style={styles.contactInfo}>
          {item.email ? (
            <View style={styles.contactItem}>
              <Text style={styles.contactLabel}>Email:</Text>
              <Text style={styles.contactValue}>{item.email}</Text>
            </View>
          ) : null}
          {item.phone ? (
            <View style={styles.contactItem}>
              <Text style={styles.contactLabel}>Phone:</Text>
              <Text style={styles.contactValue}>{item.phone}</Text>
            </View>
          ) : null}
          <View style={styles.contactItem}>
            <Text style={styles.contactLabel}>Active Policies:</Text>
            <Text style={styles.contactValue}>{item.policiesCount}</Text>
          </View>
        </View>

        <View style={styles.memberActions}>
          <Button
            mode="outlined"
            icon="file-document"
            style={styles.actionButton}
          >
            View Policies
          </Button>
          <Button
            mode="text"
            icon="pencil"
            style={styles.actionButton}
          >
            Edit
          </Button>
        </View>
      </Card.Content>
    </Card>
  );

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView style={styles.scrollView}>
        {/* Family Overview */}
        <Card style={styles.overviewCard}>
          <Card.Content>
            <Title style={styles.overviewTitle}>Family Overview</Title>
            <View style={styles.overviewStats}>
              <View style={styles.statItem}>
                <Text style={styles.statNumber}>{familyMembers.length}</Text>
                <Text style={styles.statLabel}>Family Members</Text>
              </View>
              <View style={styles.statItem}>
                <Text style={styles.statNumber}>
                  {familyMembers.reduce((sum, member) => sum + member.policiesCount, 0)}
                </Text>
                <Text style={styles.statLabel}>Total Policies</Text>
              </View>
              <View style={styles.statItem}>
                <Text style={styles.statNumber}>$2.4M</Text>
                <Text style={styles.statLabel}>Total Coverage</Text>
              </View>
            </View>
          </Card.Content>
        </Card>

        {/* Family Members List */}
        <View style={styles.membersContainer}>
          <Title style={styles.sectionTitle}>Family Members</Title>
          {familyMembers.map((member) => (
            <View key={member.id}>
              {renderFamilyMember({ item: member })}
            </View>
          ))}
        </View>

        {/* Quick Actions */}
        <Card style={styles.actionsCard}>
          <Card.Content>
            <Title style={styles.cardTitle}>Quick Actions</Title>
            <View style={styles.quickActions}>
              <Button
                mode="contained"
                icon="account-plus"
                style={styles.quickActionButton}
                buttonColor="#2E8B57"
              >
                Add Family Member
              </Button>
              <Button
                mode="outlined"
                icon="export"
                style={styles.quickActionButton}
              >
                Export Family Data
              </Button>
            </View>
          </Card.Content>
        </Card>
      </ScrollView>

      <FAB
        icon="account-plus"
        style={styles.fab}
        onPress={() => {}}
        label="Add Member"
      />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F8F9FA',
  },
  scrollView: {
    flex: 1,
  },
  overviewCard: {
    margin: 16,
    elevation: 2,
  },
  overviewTitle: {
    color: '#0A2A4E',
    textAlign: 'center',
    marginBottom: 16,
  },
  overviewStats: {
    flexDirection: 'row',
    justifyContent: 'space-around',
  },
  statItem: {
    alignItems: 'center',
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
  membersContainer: {
    paddingHorizontal: 16,
  },
  sectionTitle: {
    color: '#0A2A4E',
    marginBottom: 16,
  },
  memberCard: {
    marginBottom: 16,
    elevation: 3,
  },
  memberHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 16,
  },
  memberInfo: {
    flexDirection: 'row',
    alignItems: 'center',
    flex: 1,
  },
  memberDetails: {
    marginLeft: 16,
    flex: 1,
  },
  memberName: {
    fontSize: 20,
    color: '#0A2A4E',
    marginBottom: 8,
  },
  relationshipContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  ageText: {
    marginLeft: 12,
    color: '#666',
    fontSize: 14,
  },
  contactInfo: {
    marginBottom: 16,
  },
  contactItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 6,
  },
  contactLabel: {
    fontSize: 14,
    color: '#666',
    flex: 1,
  },
  contactValue: {
    fontSize: 14,
    color: '#0A2A4E',
    flex: 2,
    textAlign: 'right',
  },
  memberActions: {
    flexDirection: 'row',
    justifyContent: 'space-around',
  },
  actionButton: {
    flex: 1,
    marginHorizontal: 8,
  },
  actionsCard: {
    margin: 16,
    elevation: 2,
  },
  cardTitle: {
    color: '#0A2A4E',
    marginBottom: 16,
  },
  quickActions: {
    gap: 12,
  },
  quickActionButton: {
    marginBottom: 8,
  },
  fab: {
    position: 'absolute',
    margin: 16,
    right: 0,
    bottom: 0,
    backgroundColor: '#2E8B57',
  },
});