
# Build stage
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
# Install dependencies, compatible with next 16
# We use --legacy-peer-deps to avoid some conflict with next-pwa/next 16 if any
RUN npm install --legacy-peer-deps

COPY . .
# Build the application
# We use the webpack flag as configured in package.json
RUN npm run build

# Production stage
FROM node:20-alpine AS runner
WORKDIR /app

ENV NODE_ENV=production

# Don't run as root
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000

ENV PORT=3000
# set hostname to localhost
ENV HOSTNAME="0.0.0.0"

CMD ["npm", "start"]
