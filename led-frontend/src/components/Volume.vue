<template>
  <card title="Volume">
    <q-card-section class="column items-center q-mt-md">
      <q-linear-progress
        rounded
        size="xl"
        :value="volume / 100"
        color="primary"
        label="Volume"
      />
    </q-card-section>
    <q-card-section class="column items-center">
      <q-btn-group>
        <q-btn
          :color="mute ? 'grey-9' : 'grey-9'"
          icon="volume_off"
          @click="mopidy.mixer.setMute([!mute])"
        />
        <q-btn
          color="grey-9"
          icon="volume_down"
          @click="incrementVolume(-10)"
        >
          -10
        </q-btn>
        <q-btn
          color="grey-9"
          icon="volume_down"
          @click="incrementVolume(-1)"
        >
          -1
        </q-btn>
        <q-btn
          color="grey-9"
          icon="volume_up"
          @click="incrementVolume(1)"
        >
          +1
        </q-btn>
        <q-btn
          color="grey-9"
          icon="volume_up"
          @click="incrementVolume(10)"
        >
          +10
        </q-btn>
      </q-btn-group>
    </q-card-section>
  </card>
</template>

<script>
export default {
  name: 'Volume',
  props: {
    mopidy: {
      type: Object,
      required: true,
    },
  },
  data () {
    return {
      volume: 100,
      mute: false,
    };
  },
  mounted () {
    this.mopidy.on('event:volumeChanged', eObj => {
      this.volume = eObj.volume;
    });

    this.mopidy.on('event:muteChanged', eObj => {
      this.mute = eObj.mute;
    });
    this.mopidy.mixer.getMute().then(mute => { this.mute = mute; });
    this.mopidy.mixer.getVolume().then(volume => { this.volume = volume; });
  },
  methods: {
    incrementVolume (inc) {
      const v = Math.max(0, Math.min(100, this.volume + inc));
      this.mopidy.mixer.setVolume([v]);
    },
  },
};
</script>
