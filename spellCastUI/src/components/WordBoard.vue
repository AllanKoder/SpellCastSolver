<template>
  <div>
    <div v-for="row in 5" :key="row" class="grid grid-cols-5 outline-2 outline-black m-auto max-w-fit">
      <div v-for="col in 5" class="relative">
        <div>
          <input
            :key="col"
            :id="`${getKey(row, col)}`"
            v-model="matrix[row-1][col-1]"
            @change="emitMatrix"
            @click="toggleTileState(row-1, col-1)"
            @keydown="handleKeydown($event, row, col)"
            :class="getTileClass(row-1, col-1)"
            class="relative"
            type="text"
            maxlength="1"
          >
            <span class="absolute top-0 right-1 font-bold">{{ getTileIndicator(row-1, col-1) }}</span>
          </input>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';

const emit = defineEmits(['matrix-emitted', 'tile-selected'])
const props = defineProps({
  wordTiles: Array,
  startingTile: Array,
  replaced: Array,
  doubleLetterTile: String,
  doubleWordTile: String,
  tripleLetterTile: String,
});

const matrix = ref(Array(5).fill().map(() => Array(5).fill('a')));
const coloredUsedTiles = ref(props.wordTiles);
const coloredStartingTile = ref(props.startingTile);
const coloredReplacedTiles = ref(props.replaced);

const doubleLetterTile = ref(""); // Array of keys for double letter tiles
const doubleWordTile = ref(""); // Array of keys for double word tiles
const tripleLetterTile = ref(""); // Array of keys for triple letter tiles

watch(() => props.wordTiles, async (newTiles, _) => {
  coloredUsedTiles.value = newTiles
})
watch(() => props.startingTile, async (newTile, _) => {
  coloredStartingTile.value = newTile
})
watch(() => props.replaced, async (newReplacedTile, _) => {
  coloredReplacedTiles.value = newReplacedTile
})
watch(() => props.doubleLetterTile, async (newReplacedTile, _) => {
  doubleLetterTile.value = newReplacedTile
})
watch(() => props.doubleWordTile, async (newReplacedTile, _) => {
  doubleWordTile.value = newReplacedTile
})
watch(() => props.tripleLetterTile, async (newReplacedTile, _) => {
  tripleLetterTile.value = newReplacedTile
})

function emitMatrix() {
  emit('matrix-emitted', matrix.value);
}

function handleKeydown(event, row, col) {
  const key = event.key;
  const isCharacterKey = key.length === 1;

  if (isCharacterKey) {
    // Clear the current value and set the new one
    this.matrix[row-1][col-1] = key;
    if (col < 5)
    {
      event.preventDefault();
      focusInput(row, col + 1);
    }
    else if (row < 5)
    {
      event.preventDefault();
      focusInput(row + 1, 1);
    }
  } else {
    // Handle arrow keys
    if (key === 'ArrowUp' && row > 1) {
      event.preventDefault();
      focusInput(row - 1, col);
    } else if (key === 'ArrowDown' && row < 5) {
      event.preventDefault();
      focusInput(row + 1, col);
    } else if (key === 'ArrowLeft' && col > 1) {
      event.preventDefault();
      focusInput(row, col - 1);
    } else if (key === 'ArrowRight' && col < 5) {
      event.preventDefault();
      focusInput(row, col + 1);
    }
  }
}

function getTileIndicator(row, col) {
  const key = getKey(row, col);
  if (doubleLetterTile.value == (key)) {
    return 'DL';
  } else if (doubleWordTile.value == (key)) {
    return 'DW';
  } else if (tripleLetterTile.value == (key)) {
    return 'TL';
  }
  return '';
}


function getKey(row, col) {
  return `${row},${col}`;
}

function focusInput(row, col) {
  const selector = `#${CSS.escape(getKey(row, col))}`;
  const input = document.querySelector(selector);
  if (input) {
    input.focus();
  }
}

function toggleTileState(row, col) {
  emit('tile-selected', getKey(row, col));
}

function getTileClass(row, col) {
  const baseClass = 'form-input border-2 border-gray-300 w-16 h-16 text-center text-xl';

  const key = getKey(row, col);
  if (!coloredUsedTiles.value || !coloredStartingTile.value || !coloredReplacedTiles) return baseClass;

  const stringifiedStartingTile = coloredStartingTile.value.join(',');
  const stringifiedTiles = coloredUsedTiles.value.map(tile => tile.join(','));
  const stringColoredReplacedTiles = coloredReplacedTiles.value.map(tile => tile.join(','));

  if (stringifiedStartingTile.includes(key))
  {
    return `bg-blue-200 ${baseClass}`;
  }
  if (stringColoredReplacedTiles.includes(key))
  {
    return `bg-red-200 ${baseClass}`;
  }
  if (stringifiedTiles.includes(key)){
    return `bg-green-200 ${baseClass}`;
  }
  return baseClass;
}
</script>

<style>
.grid-row {
  display: flex;
}
.grid-cell {
  margin: 2px;
  width: 20px;
  height: 20px;
  text-align: center;
}
</style>
