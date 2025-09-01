FROM node:18-alpine AS builder
WORKDIR /usr/src/app

# copier package.json (et package-lock.json si présent)
COPY package*.json ./

# installer dépendances (si tu veux lockfile sécurisé: générer/committer package-lock.json puis utiliser npm ci)
RUN npm install --omit=dev --no-audit --no-fund

# copier le code
COPY . .

FROM node:18-alpine
WORKDIR /usr/src/app

# installer utilitaires nécessaires pour healthcheck
RUN apk add --no-cache curl

# créer un user non-root
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# copier les node_modules et le code depuis le builder
COPY --from=builder /usr/src/app /usr/src/app

# donner les droits au user non-root
RUN chown -R appuser:appgroup /usr/src/app
USER appuser

ENV NODE_ENV=production
EXPOSE 3000

# healthcheck interne corrige (vérifie le service dans le conteneur sur 3000)
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s \
  CMD curl -f http://localhost:3000/health || exit 1

CMD ["npm", "start"]