import NextAuth, { NextAuthOptions } from 'next-auth'
import CredentialsProvider from 'next-auth/providers/credentials'
import EmailProvider from 'next-auth/providers/email'
import { authAPI } from './api'

export const authOptions: NextAuthOptions = {
  providers: [
    CredentialsProvider({
      name: 'credentials',
      credentials: {
        email: { label: 'Email', type: 'email' },
        password: { label: 'Password', type: 'password' }
      },
      async authorize(credentials) {
        if (!credentials?.email || !credentials?.password) {
          return null
        }

        try {
          const response = await authAPI.login(credentials.email, credentials.password)
          const { access_token, token_type } = response.data

          if (access_token) {
            // Store token in localStorage (in real app, use secure storage)
            if (typeof window !== 'undefined') {
              localStorage.setItem('access_token', access_token)
            }

            return {
              id: '1',
              email: credentials.email,
              accessToken: access_token,
            }
          }
        } catch (error) {
          console.error('Login error:', error)
        }

        return null
      }
    })
    ,
    EmailProvider({
      server: process.env.RESEND_SMTP_URL || '',
      from: process.env.RESEND_FROM || 'no-reply@studynos.app'
    })
  ],
  pages: {
    signIn: '/auth/login',
    signUp: '/auth/register',
  },
  callbacks: {
    async jwt({ token, user }) {
      if (user) {
        token.accessToken = user.accessToken
      }
      return token
    },
    async session({ session, token }) {
      session.accessToken = token.accessToken
      return session
    },
  },
  session: {
    strategy: 'jwt',
  },
}

export default NextAuth(authOptions)