<template>
  <div class="carousel">
    <h2>Question {{ currentIndex + 1 }} sur {{ questions.length }}</h2>

    <progress :value="currentIndex + 1" :max="questions.length" />

    <div v-if="currentQuestion" class="question-wrapper">
      <QuestionItem :question="currentQuestion" @submitted="handleSubmit" />

      <div class="button-group">
        <button
          v-if="showNext && !isLastQuestion"
          @click="nextQuestion"
          class="next-btn"
        >
          Suivant
        </button>

        <button
          v-if="showNext && isLastQuestion"
          @click="finishQuiz"
          class="next-btn"
        >
          Terminer
        </button>
      </div>
    </div>

    <div v-else class="end-screen">
      <h2>🎉 Vous avez terminé le quiz !</h2>
      <button @click="restart" class="restart-btn">Recommencer</button>
    </div>
  </div>
</template>

<script>
import QuestionItem from './QuestionItem.vue'

export default {
  components: { QuestionItem },
  data() {
    return {
      questions: [],
      currentIndex: 0,
      showNext: false,
      finished: false,
    }
  },
  computed: {
    currentQuestion() {
      return this.questions[this.currentIndex]
    },
    isLastQuestion() {
      return this.currentIndex === this.questions.length - 1
    }
  },
  async created() {
    const res = await fetch('http://localhost:5000/questions')
    this.questions = await res.json()
  },
  methods: {
    handleSubmit() {
      this.showNext = true
    },
    nextQuestion() {
      if (!this.isLastQuestion) {
        this.currentIndex++
        this.showNext = false
      }
    },
    finishQuiz() {
      this.finished = true
      this.currentIndex = -1
    },
    restart() {
      this.currentIndex = 0
      this.showNext = false
      this.finished = false
    }
  }
}
</script>

<style scoped>
.carousel {
  max-width: 850px;
  margin: 3rem auto;
  background-color: #fff;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  color: #1f2937;
}

h2 {
  font-size: 1.5rem;
  color: #1e3a8a;
  margin-bottom: 1rem;
}

progress {
  width: 100%;
  height: 12px;
  margin-bottom: 2rem;
  appearance: none;
}

progress::-webkit-progress-bar {
  background-color: #e5e7eb;
  border-radius: 10px;
}

progress::-webkit-progress-value {
  background-color: #3b82f6;
  border-radius: 10px;
}

.question-wrapper {
  margin-top: 1rem;
}

.button-group {
  margin-top: 2rem;
}

.next-btn,
.restart-btn {
  background-color: #2563eb;
  color: white;
  padding: 0.75rem 2rem;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.3s;
}

.next-btn:hover,
.restart-btn:hover {
  background-color: #1d4ed8;
}

.end-screen {
  margin-top: 3rem;
  text-align: center;
}

.end-screen h2 {
  color: #059669;
}
</style>
