<template>
  <div>
    <el-input
        v-model="inputValue"
        :id="inputId"
        type="text"
        :placeholder="placeholder"
        class="autocomplete-input"
        ref="inputRef"
    />
  </div>
</template>

<script setup lang="ts">
import {onMounted, ref} from 'vue';

const emit = defineEmits(['placeSelected']);

const props = defineProps<{
  inputId: string;
  placeholder: string;
  countryRestriction: { country: string };
}>();

const inputRef = ref(null);
const inputValue = ref('');

function initializeAutocomplete() {
  // NEVER CHANGE!!!! THIS NEEDS TO BE INPUT FOR THE PLACES API TO WORK!!!!!
  const nativeInput = inputRef.value?.input as HTMLInputElement;

  if (nativeInput) {
    const autocomplete = new google.maps.places.Autocomplete(nativeInput, {
      types: ['geocode', 'establishment'],
      componentRestrictions: props.countryRestriction,
    });

    autocomplete.addListener('place_changed', () => {
      const place = autocomplete.getPlace();

      if (place.geometry) {
        const formattedPlace = {
          address: place.formatted_address || place.name,
          lat: place?.geometry?.location?.lat(),
          lng: place?.geometry?.location?.lng(),
          name: place.name,
          placeId: place.place_id,
        };

        emit('placeSelected', formattedPlace);
      } else {
        console.log('No details available for the input:', nativeInput.value);
      }
    });
    nativeInput.addEventListener('input', handleInputChange);
  }
  // } else if (inputRef.value) {
  //   console.error('Failed to access the native input element:', inputRef.value);
  // }
}

function handleInputChange(event: Event) {
  const target = event.target as HTMLInputElement;
  inputValue.value = target.value;

  if (!target.value) {
    emit('placeSelected', {address: '', lat: 0, lng: 0, name: '', placeId: ''});
  }
}

onMounted(() => {
  if (window.google && window.google.maps && window.google.maps.places) {
    initializeAutocomplete();
  } else {
    window.addEventListener('load', initializeAutocomplete);
  }
});

</script>

<style scoped>
.autocomplete-input {
  width: 100%;
  padding: 10px;
  font-size: 16px;
  border-radius: 4px;
  margin-bottom: 10px;
}
</style>
