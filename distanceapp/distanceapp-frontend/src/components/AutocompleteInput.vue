<template>
  <el-autocomplete
      v-model="inputValue"
      :trigger-on-focus="false"
      :placeholder="props.placeholder"
      :fetch-suggestions="fetchPlaces"
      @select="handleSelect"
      :popper-class="props.inputId"
      class="autocomplete-input"
      clearable
      @input="handleInputChange"
  />
</template>

<script setup lang="ts">
import {ref} from 'vue';
import axios from 'axios';


const emit = defineEmits(['placeSelected', 'inputCleared']);


const props = defineProps<{
  inputId: string;
  placeholder: string;
  countryRestriction: { country: string };
}>();

const inputValue = ref('');

interface Place {
  description: string;
  place_id: string;
  structured_formatting: {
    main_text: string;
    secondary_text: string;
  };
}

async function fetchPlaces(query: string, callback: (suggestions: Place[]) => void) {
  if (!query) {
    callback([]);
    return;
  }

  try {
    const response = await axios.get('http://127.0.0.1:8000/api/places-autocomplete/', {
      params: {query},
    });

    const places = response.data.predictions.map((place: Place) => ({
      value: place.description,
      place_id: place.place_id,
      structured_formatting: place.structured_formatting,
    }));

    // Update the suggestions using the callback
    callback(places);
  } catch (error) {
    console.error('Error fetching places:', error);
    callback([]);
  }
}

interface SelectedPlace {
  place_id: string;
}

async function handleSelect(item: SelectedPlace) {
  try {
    // Fetch the selected place details including lat and lng
    const response = await axios.get('http://127.0.0.1:8000/api/get-place-details/', {
      params: {place_id: item.place_id},
    });

    // Emit the selected place details to the parent component
    emit('placeSelected', response.data);
  } catch (error) {
    console.error('Error fetching place details:', error);
  }
}

function handleInputChange(value: string) {
  inputValue.value = value;
  if (!value) {
    emit('inputCleared', '');
  }
}

</script>

<style scoped>
.autocomplete-input {
  width: 100%;
  padding: 10px;
  font-size: 18px;
  border-radius: 4px;
  margin-bottom: 10px;
}
</style>
