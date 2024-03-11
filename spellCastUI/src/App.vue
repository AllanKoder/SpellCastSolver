<script setup>
import HelloWorld from './components/HelloWorld.vue'
import WordBoard from './components/WordBoard.vue'

import { ref, watch } from 'vue';
import { getScore } from './utils/getScore';

const matrix = ref(null)
const currentErrors = ref(null)

const doubleWord = ref("")

function setMatrix(newMatrix) {
  matrix.value = newMatrix
};

async function getBestWords(){
  console.log(matrix.value)
  const result = await getScore(matrix.value)
  
  console.log(result)
  if (result.error) {
    currentErrors.value = result.error
    return
  } 
  else
  {
    currentErrors.value = null
  }
  console.log(result.error)
  console.log(result.data)
}

</script>

<template>
  <HelloWorld/>
  
  <h5 v-if="currentErrors">{{ currentErrors }}</h5>
  <div class="flex flex-2 gap-5">
    
    <WordBoard @matrix-emitted = "setMatrix" ></WordBoard>
  </div>

  <button @click="getBestWords" class="m-5 bg-slate-200">Get Score</button>
</template>
