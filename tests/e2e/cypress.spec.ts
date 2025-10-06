// cypress/e2e/app.cy.ts

describe('Student Productivity App E2E Tests', () => {
  beforeEach(() => {
    // Visit the landing page
    cy.visit('http://localhost:3000')
  })

  describe('Landing Page', () => {
    it('should display the landing page correctly', () => {
      cy.contains('Master Your Academic Journey')
      cy.contains('Get Started')
      cy.contains('Learn More')
    })

    it('should navigate to dashboard when Get Started is clicked', () => {
      cy.contains('Get Started').click()
      cy.url().should('include', '/app/dashboard')
    })

    it('should display feature sections', () => {
      cy.contains('Smart Calendar')
      cy.contains('AI Flashcards')
      cy.contains('GPA Prediction')
      cy.contains('Study Planner')
    })
  })

  describe('Authentication Flow', () => {
    it('should handle login flow', () => {
      cy.visit('/app/dashboard')
      
      // Should redirect to login if not authenticated
      // (This would need actual auth implementation)
      
      // Mock login
      cy.get('[data-testid="email-input"]').type('test@example.com')
      cy.get('[data-testid="password-input"]').type('password123')
      cy.get('[data-testid="login-button"]').click()
      
      // Should redirect to dashboard after successful login
      cy.url().should('include', '/app/dashboard')
    })

    it('should handle registration flow', () => {
      cy.visit('/auth/register')
      
      cy.get('[data-testid="name-input"]').type('John Doe')
      cy.get('[data-testid="email-input"]').type('john@example.com')
      cy.get('[data-testid="password-input"]').type('password123')
      cy.get('[data-testid="confirm-password-input"]').type('password123')
      cy.get('[data-testid="register-button"]').click()
      
      // Should redirect to dashboard after successful registration
      cy.url().should('include', '/app/dashboard')
    })
  })

  describe('Dashboard', () => {
    beforeEach(() => {
      // Mock authentication
      cy.window().then((win) => {
        win.localStorage.setItem('access_token', 'mock-token')
      })
      cy.visit('/app/dashboard')
    })

    it('should display dashboard stats', () => {
      cy.contains('Current GPA')
      cy.contains('Active Classes')  
      cy.contains('Upcoming Deadlines')
      cy.contains('Study Streak')
    })

    it('should display recent assignments', () => {
      cy.contains('Recent Assignments')
      cy.get('[data-testid="assignment-item"]').should('have.length.at.least', 1)
    })

    it('should display calendar widget', () => {
      cy.contains('Calendar')
      cy.get('[data-testid="calendar-widget"]').should('be.visible')
    })
  })

  describe('Classes Management', () => {
    beforeEach(() => {
      cy.window().then((win) => {
        win.localStorage.setItem('access_token', 'mock-token')
      })
      cy.visit('/app/classes')
    })

    it('should display classes list', () => {
      cy.contains('Classes')
      cy.get('[data-testid="add-class-button"]').should('be.visible')
    })

    it('should allow creating a new class', () => {
      cy.get('[data-testid="add-class-button"]').click()
      
      cy.get('[data-testid="class-name-input"]').type('Computer Science 101')
      cy.get('[data-testid="class-code-input"]').type('CS101')
      cy.get('[data-testid="professor-input"]').type('Dr. Smith')
      cy.get('[data-testid="credits-input"]').type('3')
      
      cy.get('[data-testid="save-class-button"]').click()
      
      cy.contains('Computer Science 101')
    })

    it('should allow viewing class details', () => {
      cy.get('[data-testid="class-item"]').first().click()
      
      cy.url().should('include', '/app/classes/')
      cy.contains('Course Description')
      cy.contains('Assignments')
    })
  })

  describe('Calendar', () => {
    beforeEach(() => {
      cy.window().then((win) => {
        win.localStorage.setItem('access_token', 'mock-token')
      })
      cy.visit('/app/calendar')
    })

    it('should display calendar view', () => {
      cy.contains('Calendar')
      cy.get('[data-testid="calendar-widget"]').should('be.visible')
    })

    it('should display upcoming events', () => {
      cy.contains('Upcoming Events')
      cy.get('[data-testid="event-item"]').should('exist')
    })

    it('should allow adding new events', () => {
      cy.get('[data-testid="add-event-button"]').click()
      
      // Test event creation form
      cy.get('[data-testid="event-title-input"]').type('Study Session')
      cy.get('[data-testid="event-date-input"]').type('2024-03-15')
      cy.get('[data-testid="event-time-input"]').type('14:00')
      
      cy.get('[data-testid="save-event-button"]').click()
      
      cy.contains('Study Session')
    })
  })

  describe('Flashcards', () => {
    beforeEach(() => {
      cy.window().then((win) => {
        win.localStorage.setItem('access_token', 'mock-token')
      })
      cy.visit('/app/flashcards')
    })

    it('should display flashcard viewer', () => {
      cy.get('[data-testid="flashcard-viewer"]').should('be.visible')
    })

    it('should allow flipping flashcards', () => {
      cy.get('[data-testid="flashcard"]').click()
      cy.contains('Answer:')
    })

    it('should allow marking answers as correct/incorrect', () => {
      cy.get('[data-testid="flashcard"]').click()
      cy.get('[data-testid="correct-button"]').click()
      
      // Should advance to next card
      cy.get('[data-testid="flashcard-counter"]').should('contain', '2 of')
    })
  })

  describe('GPA Tracking', () => {
    beforeEach(() => {
      cy.window().then((win) => {
        win.localStorage.setItem('access_token', 'mock-token')
      })
      cy.visit('/app/gpa')
    })

    it('should display current GPA', () => {
      cy.contains('Current GPA')
      cy.get('[data-testid="current-gpa"]').should('be.visible')
    })

    it('should show GPA prediction', () => {
      cy.contains('GPA Prediction')
      cy.get('[data-testid="target-gpa-input"]').type('3.8')
      cy.get('[data-testid="predict-button"]').click()
      
      cy.contains('recommendation')
    })

    it('should display grade breakdown by class', () => {
      cy.contains('Grade Breakdown')
      cy.get('[data-testid="class-grade-item"]').should('have.length.at.least', 1)
    })
  })

  describe('Responsive Design', () => {
    it('should work on mobile viewport', () => {
      cy.viewport('iphone-6')
      cy.visit('/')
      
      cy.contains('Master Your Academic Journey')
      cy.get('[data-testid="mobile-menu-button"]').should('be.visible')
    })

    it('should work on tablet viewport', () => {
      cy.viewport('ipad-2')
      cy.visit('/app/dashboard')
      
      cy.contains('Dashboard')
      cy.get('[data-testid="sidebar"]').should('be.visible')
    })
  })

  describe('Error Handling', () => {
    it('should handle network errors gracefully', () => {
      // Mock network failure
      cy.intercept('GET', '/api/v1/classes/', { forceNetworkError: true })
      
      cy.window().then((win) => {
        win.localStorage.setItem('access_token', 'mock-token')
      })
      cy.visit('/app/classes')
      
      cy.contains('Error loading classes')
    })

    it('should handle authentication errors', () => {
      // Mock 401 response
      cy.intercept('GET', '/api/v1/classes/', { statusCode: 401 })
      
      cy.window().then((win) => {
        win.localStorage.setItem('access_token', 'invalid-token')
      })
      cy.visit('/app/classes')
      
      // Should redirect to login
      cy.url().should('include', '/auth/login')
    })
  })
})