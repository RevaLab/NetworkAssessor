<template>
    <div class="bug-report">
        <div id="bug-report-button">
            <button class="button is-light is-rounded" v-on:click="showBugReportForm">Report Bug</button>
        </div>
        <modal name="bug-report" transition="pop-out" :width="modalWidth" :height="400">
            <div id="bug-report-form" v-if="!reportSent">
                <div class="field">
                  <label class="label">What happened:*</label>
                  <div class="control">
                    <textarea class="textarea" placeholder="Textarea" v-model="report"></textarea>
                  </div>
                </div>

                <div class="field input-field">
                    <label class="label">E-mail:</label>
                    <div class="control">
                        <input class="input" type="email" placeholder="Optional" value="" v-model="email">
                    </div>
                </div>

                <div class="field input-field">
                    <label class="label">Name:</label>
                    <div class="control">
                        <input class="input" type="email" placeholder="Optional" value="" v-model="name">
                    </div>
                </div>

                <button class="button" v-on:click="submitReport">Send Report</button>
            </div>
            <div id="bug-report-sent" v-if="reportSent">
                <p id="thank-you-message">Thanks for sending your bug report for review!</p>
            </div>
        </modal>
    </div>
</template>

<script>
    let MODAL_WIDTH = 656;

    export default {
        name: "bug-report",
        data() {
            return {
                modalWidth: MODAL_WIDTH,
                report: '',
                email: '',
                name: '',
                reportSent: false
            }
        },
        created () {
            this.modalWidth = window.innerWidth < MODAL_WIDTH
              ? MODAL_WIDTH / 2
              : MODAL_WIDTH
        },
        methods: {
            showBugReportForm() {
                this.reportSent = false;
                this.$modal.show('bug-report');
            },
            submitReport() {

                if (!this.report) {
                    alert('Please include a description of the bug.');
                    return;
                }

                this.$store.dispatch('submitBugReport', {
                    report: this.report,
                    email: this.email,
                    name: this.name
                });

                this.reportSent = true;
            }
        }
    }
</script>

<style scoped>
    #bug-report-button {
        position: fixed;
        z-index: 1;
        bottom:20px;
        right:20px;
    }

    .bug-report #bug-report-form {
        width: 80%;
        margin: 20px auto;
    }
</style>
