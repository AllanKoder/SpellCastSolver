<script setup>
import WordBoard from './components/WordBoard.vue'

import { ref } from 'vue';
import { getScore } from './utils/getScore';

const matrix = ref(null)
const currentErrors = ref(null)
const bestWord = ref("Get the Best Word!")
const bestScore = ref("")
const highlightedWords = ref([])

const replacedTiles = ref([])
const startingSearchTile = ref([])

const subsitutions = ref(0)

const mode = ref('none');
const doubleLetterTile = ref("");
const doubleWordTile = ref("");
const tripleLetterTile = ref("");

function setDoubleLetterMode() {
  mode.value = 'double-letter';
}

function setDoubleWordMode() {
  mode.value = 'double-word';
}

function setTripleLetterMode() {
  mode.value = 'triple-letter';
}

function setNoneMode() {
  mode.value = 'none';
}

function setNormalMode() {
  mode.value = 'normal';
}

function handleTileSelected(tile) {
  if (mode.value === 'double-letter') {
    doubleLetterTile.value = tile;
    mode.value = 'normal';
  } else if (mode.value === 'double-word') {
    doubleWordTile.value = tile;
    mode.value = 'normal';
  } else if (mode.value === 'triple-letter') {
    tripleLetterTile.value = tile;
    mode.value = 'normal';
  }
  else if (mode.value == "none")
  {
    if (doubleLetterTile.value == tile)
    {
      doubleLetterTile.value = ""
    }
    if (doubleWordTile.value == tile)
    {
      doubleWordTile.value = ""
    }
    if (tripleLetterTile.value == tile)
    {
      tripleLetterTile.value = ""
    }
  }
}
function setMatrix(newMatrix) {
  matrix.value = newMatrix
};

async function getBestWords(){
  let doubleLetter = []
  let doubleWord = []
  let tripleLetter = []
  if (doubleLetterTile.value != "") doubleLetter = doubleLetterTile.value.split(",").map(item => parseInt(item))
  if (doubleWordTile.value != "") doubleWord = doubleWordTile.value.split(",").map(item => parseInt(item))
  if (tripleLetterTile.value != "") tripleLetter = tripleLetterTile.value.split(",").map(item => parseInt(item))

  const result = await getScore(matrix.value, subsitutions.value, doubleLetter, doubleWord, tripleLetter)
  
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
  replacedTiles.value = result.data.replaced
  startingSearchTile.value = result.data.starting_tile
  bestScore.value = result.data.score
}

</script>

<template>
  <h1 class="m-3" v-if="bestWord">{{ bestWord }}</h1>
  <h2 class="m-3" v-if="bestScore"><b>Score: </b>{{ bestScore }}</h2>

  <h5 v-if="currentErrors">{{ currentErrors }}</h5>
  <div class="mx-auto">
    <WordBoard 
    @matrix-emitted = "setMatrix" 
    @tile-selected="handleTileSelected"
    :wordTiles="highlightedWords"
    :replaced="replacedTiles"
    :startingTile="startingSearchTile"
    :doubleLetterTile="doubleLetterTile"
    :doubleWordTile="doubleWordTile"
    :tripleLetterTile="tripleLetterTile"
    </WordBoard>
  </div>
  <div class="flex flex-row m-5 gap-4 content-end w-full mx-auto">
    <div class="mx-auto">
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
    <div class="m-auto mx-auto">
      <h5 class="font-bold">Tile Type</h5>
      <div class="flex gap-3 m-auto">
        <button @click="setDoubleLetterMode">DL</button>
        <button @click="setDoubleWordMode">DW</button>
        <button @click="setTripleLetterMode">TL</button>
        <button @click="setNormalMode">Normal</button>
        <button @click="setNoneMode" class="bg-red-100">Clear</button>
      </div>
    </div>
  </div>

  <button @click="getBestWords" class="m-5 bg-slate-200">Get Score</button>
</template>
