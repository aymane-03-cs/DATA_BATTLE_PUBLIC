<template>
  <div class="question-form">
    <h3>{{ question.question }}</h3>

    <!-- QCM -->
    <div v-if="question.type === 'qcm'" class="qcm-options">
      <label v-for="(opt, key) in question.options" :key="key" class="option">
        <input type="radio" :value="key" v-model="answer" />
        <strong>{{ key }}.</strong> {{ opt }}
      </label>
    </div>

    <!-- Question ouverte -->
    <div v-else>
      <textarea
        v-model="answer"
        placeholder="Écrivez votre réponse ici..."
        rows="5"
      ></textarea>
    </div>

    <button @click="submit">Valider</button>

    <div v-if="result" class="result-block">
      <!-- QCM feedback -->
      <p v-if="question.type === 'qcm'">
         Votre réponse est
        <strong :class="{ correct: result.correct, wrong: !result.correct }">
          {{ result.correct ? 'correcte' : 'incorrecte' }}
        </strong>
      </p>

      <!-- Question ouverte feedback -->
      <Feedback v-if="question.type === 'ouverte'" :content="result.feedback" />
    </div>
  </div>
</template>

<script>
import Feedback from './Feedback.vue'

export default {
  props: ["question"],
  components: { Feedback },
  data() {
    return {
      answer: "",
      result: null
    }
  },
  watch: {
    question() {
      this.answer = ""
      this.result = null
    }
  },
  methods: {
    async submit() {
      const res = await fetch("http://localhost:5000/submit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          type: this.question.type,
          question: this.question.question,
          answer: this.answer
        })
      })

      this.result = await res.json()
      this.$emit("submitted")
    }
  }
}
</script>

<style scoped>
.question-form {
  background: #ffffff;
  padding: 1.8rem;
  border-radius: 10px;
  color: #1f2937;
  border: 1px solid #e5e7eb;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
  margin-bottom: 2rem;
}

h3 {
  font-size: 1.3rem;
  color: #1e3a8a;
  margin-bottom: 1rem;
}

.qcm-options {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-top: 1rem;
}

.option {
  background: #f3f4f6;
  padding: 0.6rem;
  border-radius: 6px;
  border: 1px solid #d1d5db;
}

textarea {
  width: 100%;
  padding: 0.9rem;
  margin-top: 1rem;
  background: #f9fafb;
  color: #1f2937;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  font-family: 'Open Sans', sans-serif;
  resize: vertical;
}

button {
  margin-top: 1.5rem;
  padding: 0.7rem 2rem;
  font-weight: 600;
  font-size: 1rem;
  background: #2563eb;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.3s;
}

button:hover {
  background: #1d4ed8;
}

.result-block {
  margin-top: 1.5rem;
  font-size: 1rem;
}

.correct {
  color: #22c55e;
}
.wrong {
  color: #ef4444;
}
</style>
