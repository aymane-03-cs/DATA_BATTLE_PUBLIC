<template>
  <div class="intro-card">
    <h1>Bienvenue sur PrepBrevet 🎓</h1>
    <p>
      Cette plateforme vous aide à vous entraîner efficacement pour le brevet.
      Retrouvez des QCM, des questions ouvertes corrigées automatiquement, et suivez vos progrès en temps réel.
    </p>
    <p class="cta">Commencez dès maintenant votre entraînement !</p>
  </div>
</template>

<script setup>
// Aucun besoin de script pour un composant statique
</script>

<style scoped>
.intro-card {
  background-color: #ffffff;
  border-left: 5px solid #3b82f6;
  border-radius: 12px;
  padding: 2rem;
  margin: 2rem auto;
  max-width: 800px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.intro-card h1 {
  font-size: 1.8rem;
  color: #1e3a8a;
  margin-bottom: 1rem;
}

.intro-card p {
  font-size: 1.05rem;
  line-height: 1.6;
  color: #374151;
}

.cta {
  margin-top: 1rem;
  font-weight: bold;
  color: #2563eb;
}
</style>
