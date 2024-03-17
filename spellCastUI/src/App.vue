<script setup>
import WordBoard from './components/WordBoard.vue'

import { ref, watch } from 'vue';
import { getScore } from './utils/getScore';

const matrix = ref(null)
const currentErrors = ref(null)
const bestWord = ref("Get the Best Word!")
const highlightedWords = ref([])
const startingSearchTile = ref([])

const subsitutions = ref(0)
const doubleWord = ref("")

function setMatrix(newMatrix) {
  matrix.value = newMatrix
};

async function getBestWords(){
  const result = await getScore(matrix.value, subsitutions.value)
  
  if (result.error) {
    currentErrors.value = result.error
    return
  } 
  else
  {
    currentErrors.value = null
  }

  bestWord.value = result.data.word
  highlightedWords.value = result.data.tiles
  startingSearchTile.value = result.data.starting_tile

}

</script>

<template>
  <h1 class="m-3" v-if="bestWord">{{ bestWord }}</h1>

  <h5 v-if="currentErrors">{{ currentErrors }}</h5>
  <div class="mx-auto">
    <WordBoard 
    @matrix-emitted = "setMatrix" 
    :wordTiles="highlightedWords"
    :startingTile="startingSearchTile"
    </WordBoard>
  </div>

  <div class="flex flex-row m-5 gap-4 content-end w-full">
    <div>
      <h5 class="font-bold"># of subsitutions</h5>
      <select v-model="subsitutions">
        <option>0</option>
        <option>1</option>
        <option>2</option>
        <option>3</option>
        <option>4</option>
        <option>5</option>
      </select>
    </div>
  </div>

  <button @click="getBestWords" class="m-5 bg-slate-200">Get Score</button>
</template>
