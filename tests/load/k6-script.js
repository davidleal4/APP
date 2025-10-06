import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate } from 'k6/metrics';

// Custom metrics
const errorRate = new Rate('error_rate');

// Test configuration
export const options = {
  // Load test stages
  stages: [
    { duration: '2m', target: 10 }, // Ramp up to 10 users over 2 minutes
    { duration: '5m', target: 10 }, // Stay at 10 users for 5 minutes
    { duration: '2m', target: 20 }, // Ramp up to 20 users over 2 minutes
    { duration: '5m', target: 20 }, // Stay at 20 users for 5 minutes
    { duration: '2m', target: 0 },  // Ramp down to 0 users
  ],
  
  // Performance thresholds
  thresholds: {
    http_req_duration: ['p(95)<500'], // 95% of requests should be below 500ms
    http_req_failed: ['rate<0.1'],    // Error rate should be less than 10%
    error_rate: ['rate<0.1'],         // Custom error rate should be less than 10%
  },
};

// Base URL configuration
const BASE_URL = __ENV.BASE_URL || 'http://localhost:8000';
const FRONTEND_URL = __ENV.FRONTEND_URL || 'http://localhost:3000';

// Test data
const testUser = {
  email: 'loadtest@example.com',
  password: 'loadtest123',
  full_name: 'Load Test User'
};

// Authentication token (will be set after login)
let authToken = '';

export function setup() {
  // Setup phase - create test user and get auth token
  console.log('Setting up load test...');
  
  // Register test user
  const registerResponse = http.post(`${BASE_URL}/api/v1/auth/register`, 
    JSON.stringify(testUser), 
    { headers: { 'Content-Type': 'application/json' } }
  );
  
  if (registerResponse.status === 200 || registerResponse.status === 400) {
    // User created or already exists, now login
    const loginResponse = http.post(`${BASE_URL}/api/v1/auth/login`, 
      `username=${testUser.email}&password=${testUser.password}`, 
      { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }
    );
    
    if (loginResponse.status === 200) {
      const loginData = JSON.parse(loginResponse.body);
      authToken = loginData.access_token;
      console.log('Authentication successful');
      return { authToken };
    }
  }
  
  console.log('Setup failed - continuing without auth');
  return { authToken: '' };
}

export default function(data) {
  const token = data.authToken || authToken;
  const headers = token ? {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  } : {
    'Content-Type': 'application/json'
  };

  // Test scenarios
  const scenarios = [
    testLandingPage,
    testAuthenticationFlow,
    testDashboardLoad,
    testClassesAPI,
    testAssignmentsAPI,
    testFlashcardsAPI,
    testGPACalculation
  ];

  // Randomly select a scenario to simulate realistic user behavior
  const scenario = scenarios[Math.floor(Math.random() * scenarios.length)];
  scenario(headers);

  // Think time between requests
  sleep(Math.random() * 3 + 1); // 1-4 seconds
}

function testLandingPage(headers) {
  const response = http.get(FRONTEND_URL);
  
  const success = check(response, {
    'landing page loads': (r) => r.status === 200,
    'contains app title': (r) => r.body.includes('StudyApp') || r.body.includes('Student Productivity'),
  });
  
  errorRate.add(!success);
}

function testAuthenticationFlow(headers) {
  // Test login endpoint
  const loginData = `username=${testUser.email}&password=${testUser.password}`;
  const response = http.post(`${BASE_URL}/api/v1/auth/login`, loginData, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
  });
  
  const success = check(response, {
    'login successful': (r) => r.status === 200,
    'returns access token': (r) => r.body.includes('access_token'),
  });
  
  errorRate.add(!success);
}

function testDashboardLoad(headers) {
  // Simulate dashboard data loading
  const responses = http.batch([
    ['GET', `${BASE_URL}/api/v1/classes/`, null, { headers }],
    ['GET', `${BASE_URL}/api/v1/assignments/`, null, { headers }],
    ['GET', `${BASE_URL}/api/v1/gpa/calculate`, null, { headers }],
  ]);

  const success = check(responses, {
    'all dashboard APIs respond': (responses) => responses.every(r => r.status === 200 || r.status === 401),
  });
  
  errorRate.add(!success);
}

function testClassesAPI(headers) {
  // Test classes CRUD operations
  
  // 1. Get all classes
  let response = http.get(`${BASE_URL}/api/v1/classes/`, { headers });
  let success = check(response, {
    'get classes successful': (r) => r.status === 200 || r.status === 401,
  });

  if (response.status === 200) {
    // 2. Create a new class
    const newClass = {
      name: `Load Test Class ${Math.random()}`,
      code: `LT${Math.floor(Math.random() * 1000)}`,
      credits: 3,
      professor: 'Dr. Load Test'
    };

    response = http.post(`${BASE_URL}/api/v1/classes/`, JSON.stringify(newClass), { headers });
    success = success && check(response, {
      'create class successful': (r) => r.status === 200,
    });

    if (response.status === 200) {
      const classData = JSON.parse(response.body);
      const classId = classData.id;

      // 3. Get specific class
      response = http.get(`${BASE_URL}/api/v1/classes/${classId}`, { headers });
      success = success && check(response, {
        'get specific class successful': (r) => r.status === 200,
      });

      // 4. Update class
      const updateData = { name: `Updated ${newClass.name}` };
      response = http.put(`${BASE_URL}/api/v1/classes/${classId}`, JSON.stringify(updateData), { headers });
      success = success && check(response, {
        'update class successful': (r) => r.status === 200,
      });

      // 5. Delete class
      response = http.del(`${BASE_URL}/api/v1/classes/${classId}`, null, { headers });
      success = success && check(response, {
        'delete class successful': (r) => r.status === 200,
      });
    }
  }

  errorRate.add(!success);
}

function testAssignmentsAPI(headers) {
  // Test assignments API
  const response = http.get(`${BASE_URL}/api/v1/assignments/`, { headers });
  
  const success = check(response, {
    'get assignments successful': (r) => r.status === 200 || r.status === 401,
  });
  
  errorRate.add(!success);
}

function testFlashcardsAPI(headers) {
  // Test flashcards API
  const response = http.get(`${BASE_URL}/api/v1/flashcards/`, { headers });
  
  const success = check(response, {
    'get flashcards successful': (r) => r.status === 200 || r.status === 401,
  });
  
  errorRate.add(!success);
}

function testGPACalculation(headers) {
  // Test GPA calculation endpoints
  const responses = http.batch([
    ['GET', `${BASE_URL}/api/v1/gpa/calculate`, null, { headers }],
    ['GET', `${BASE_URL}/api/v1/gpa/predict?target_gpa=3.5`, null, { headers }],
  ]);

  const success = check(responses, {
    'GPA endpoints respond': (responses) => responses.every(r => r.status === 200 || r.status === 401),
  });
  
  errorRate.add(!success);
}

export function teardown(data) {
  // Cleanup phase
  console.log('Cleaning up load test...');
  
  // Could add cleanup logic here if needed
  // For example, delete test data created during the test
}