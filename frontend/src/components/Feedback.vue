<template>
  <div class="feedback" v-html="rendered" />
</template>

<script>
import { marked } from 'marked'

export default {
  props: ["content"],
  computed: {
    rendered() {
      return marked(this.content || '')
    }
  }
}
</script>

<style scoped>
.feedback {
  background: #ffffff;
  color: #2c3e50;
  padding: 1.5rem;
  margin-top: 1.5rem;
  border-left: 6px solid #3b82f6; /* Accent éducatif */
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  font-size: 1rem;
  line-height: 1.6;
}

.feedback h1, .feedback h2, .feedback h3 {
  color: #1e3a8a;
}

.feedback code {
  background: #f3f4f6;
  padding: 2px 6px;
  border-radius: 4px;
  font-family: monospace;
}
</style>
