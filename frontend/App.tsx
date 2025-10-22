import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { createStackNavigator } from '@react-navigation/stack';
import { Provider as PaperProvider } from 'react-native-paper';
import { Ionicons } from '@expo/vector-icons';
import { StatusBar } from 'expo-status-bar';
import { SafeAreaProvider } from 'react-native-safe-area-context';

// Import screens
import DashboardScreen from './src/screens/DashboardScreen';
import PoliciesScreen from './src/screens/PoliciesScreen';
import FamilyScreen from './src/screens/FamilyScreen';
import SettingsScreen from './src/screens/SettingsScreen';
import LoginScreen from './src/screens/LoginScreen';

// InsurAssure AI Theme
const theme = {
  colors: {
    primary: '#0A2A4E',     // Deep Blue
    accent: '#2E8B57',      // Safe Green
    warning: '#FDB813',     // Gold
    background: '#F8F9FA',  // Light Gray
    surface: '#FFFFFF',
    text: '#2C3E50',
    placeholder: '#7F8C8D',
    disabled: '#BDC3C7',
    backdrop: 'rgba(0,0,0,0.5)',
  },
};

const Tab = createBottomTabNavigator();
const Stack = createStackNavigator();

function MainTabs() {
  return (
    <Tab.Navigator
      screenOptions={({ route }) => ({
        tabBarIcon: ({ focused, color, size }) => {
          let iconName: keyof typeof Ionicons.glyphMap;

          if (route.name === 'Dashboard') {
            iconName = focused ? 'home' : 'home-outline';
          } else if (route.name === 'Policies') {
            iconName = focused ? 'document-text' : 'document-text-outline';
          } else if (route.name === 'Family') {
            iconName = focused ? 'people' : 'people-outline';
          } else {
            iconName = focused ? 'settings' : 'settings-outline';
          }

          return <Ionicons name={iconName} size={size} color={color} />;
        },
        tabBarActiveTintColor: theme.colors.primary,
        tabBarInactiveTintColor: 'gray',
        tabBarStyle: {
          backgroundColor: theme.colors.surface,
          borderTopColor: theme.colors.primary,
          borderTopWidth: 1,
        },
        headerStyle: {
          backgroundColor: theme.colors.primary,
        },
        headerTintColor: '#FFFFFF',
        headerTitleStyle: {
          fontWeight: 'bold',
        },
      })}
    >
      <Tab.Screen 
        name="Dashboard" 
        component={DashboardScreen}
        options={{ title: 'InsurAssure AI' }}
      />
      <Tab.Screen 
        name="Policies" 
        component={PoliciesScreen}
        options={{ title: 'My Policies' }}
      />
      <Tab.Screen 
        name="Family" 
        component={FamilyScreen}
        options={{ title: 'Family Members' }}
      />
      <Tab.Screen 
        name="Settings" 
        component={SettingsScreen}
        options={{ title: 'Settings' }}
      />
    </Tab.Navigator>
  );
}

export default function App() {
  const [isLoggedIn, setIsLoggedIn] = React.useState(false);

  return (
    <SafeAreaProvider>
      <PaperProvider theme={theme}>
        <StatusBar style="light" backgroundColor={theme.colors.primary} />
        <NavigationContainer>
          <Stack.Navigator screenOptions={{ headerShown: false }}>
            {isLoggedIn ? (
              <Stack.Screen name="Main" component={MainTabs} />
            ) : (
              <Stack.Screen name="Login">
                {(props) => <LoginScreen {...props} onLogin={() => setIsLoggedIn(true)} />}
              </Stack.Screen>
            )}
          </Stack.Navigator>
        </NavigationContainer>
      </PaperProvider>
    </SafeAreaProvider>
  );
}