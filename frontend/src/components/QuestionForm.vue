<template>
  <div class="question-item">
    <h3>Question {{ question.number }}</h3>
    <p class="question-text">{{ question.question }}</p>

    <!-- QCM -->
    <div v-if="question.type === 'qcm'" class="qcm-options">
      <label
        v-for="(option, key) in question.options"
        :key="key"
        class="option"
      >
        <input type="radio" :value="key" v-model="answer" />
        <strong>{{ key }}.</strong> {{ option }}
      </label>
    </div>

    <!-- Question ouverte -->
    <div v-else>
      <textarea
        v-model="answer"
        rows="5"
        placeholder="Écrivez votre réponse ici..."
      ></textarea>
    </div>

    <button @click="submitAnswer">Valider</button>

    <!-- Résultat / feedback -->
    <div v-if="result" class="feedback">
      <!-- QCM -->
      <p v-if="question.type === 'qcm'">
        Votre réponse est
        <strong :class="{ correct: result.correct, wrong: !result.correct }">
          {{ result.correct ? 'correcte' : 'incorrecte' }}
        </strong>
      </p>

      <!-- Question ouverte -->
      <Feedback v-if="question.type === 'ouverte'" :content="result.feedback" />
    </div>
  </div>
</template>

<script>
import Feedback from "./Feedback.vue";

export default {
  props: ["question"],
  components: { Feedback },
  data() {
    return {
      answer: "",
      result: null,
    };
  },
  methods: {
    async submitAnswer() {
      const res = await fetch("http://localhost:5000/submit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          type: this.question.type,
          question: this.question.question,
          answer: this.answer,
        }),
      });

      const data = await res.json();
      this.result = data;
      this.$emit("submitted");
    },
  },
};
</script>

<style scoped>
.question-item {
  background: #ffffff;
  border: 1px solid #e5e7eb;
  padding: 1.5rem;
  border-radius: 10px;
  color: #1f2937;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
  margin-bottom: 2rem;
}

h3 {
  color: #1e3a8a;
  margin-bottom: 0.5rem;
}

.question-text {
  font-size: 1.1rem;
  margin-bottom: 1rem;
}

textarea {
  width: 100%;
  padding: 0.8rem;
  background: #f9fafb;
  color: #1f2937;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  font-family: 'Open Sans', sans-serif;
  margin-top: 1rem;
}

button {
  margin-top: 1rem;
  padding: 0.6rem 1.5rem;
  font-weight: 600;
  font-size: 1rem;
  background: #2563eb;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.2s;
}

button:hover {
  background: #1d4ed8;
}

.qcm-options {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-top: 1rem;
}

.option {
  background: #f3f4f6;
  padding: 0.6rem;
  border-radius: 6px;
  border: 1px solid #d1d5db;
  cursor: pointer;
}

.option input {
  margin-right: 0.5rem;
}

.feedback {
  margin-top: 1.5rem;
}

.correct {
  color: #22c55e;
}
.wrong {
  color: #ef4444;
}
</style>
