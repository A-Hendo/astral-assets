# Privacy Policy for Astral Keyboard

**Last Updated:** August 31, 2026

**Astral Keyboard** ("Astral", "we", "us", or "our") is committed to protecting your privacy. This Privacy Policy explains how our Android keyboard application handles your data, permissions, and security.

Astral is built with a **privacy-first architecture**: unlike traditional cloud-connected keyboards, all text processing, autocorrection, and learning occur entirely locally on your device.

---

## 1. Typing & Keystroke Data

* **Local Processing:** All keystrokes, words, characters, numbers, passwords, and gesture swipe trajectories are processed in-memory directly on your device using our native on-device engine.
* **No Cloud Transmission:** We **do not** log, track, record, or transmit your keystrokes, personal messages, credit card numbers, or passwords over the internet.
* **Personal Dictionary:** Any learned words or personal autocorrect preferences are stored exclusively in your device's local application storage and never leave your phone.

---

## 2. Voice Typing & Audio

* **Microphone Access:** When you explicitly tap the microphone button on the keyboard, Astral utilizes the Android system's speech recognition interface (`RECORD_AUDIO`) to convert your spoken words into text.
* **Audio Handling:** Voice signals are handled by your device's default system speech provider (such as Google Speech Services) in accordance with your device's operating system settings. Astral does not record, log, store, or transmit your audio recordings to any external server.

---

## 3. System Permissions

Astral requests only the minimum Android permissions necessary to provide keyboard functionality:

| Permission | Purpose |
|---|---|
| `RECORD_AUDIO` | Enables optional voice-to-text transcription when the microphone key is pressed. |
| `READ_USER_DICTIONARY` / `WRITE_USER_DICTIONARY` | Allows synchronization with Android's system user spelling dictionary for personalized suggestions. |
| `VIBRATE` | Provides tactile haptic feedback during key presses and gesture navigation. |
| `INTERNET` | Used solely to download user-requested language dictionaries, sound packs, themes, and to fetch third-party advertisements. **No keystrokes, text inputs, or voice data are ever transmitted.** |

---

## 4. Third-Party Advertising Services

Astral may integrate third-party advertising SDKs, including the **Google Mobile Ads (AdMob) SDK**, to serve banner or rewarded video ads.

* AdMob may collect and process device identifiers, advertising IDs, and diagnostic information in accordance with [Google's Privacy Policy](https://policies.google.com/privacy).
* **No typing data, keystrokes, voice inputs, or user dictionary contents are ever shared with or accessible to the advertising SDK.**

---

## 5. Data Retention & Deletion

* Because Astral does not maintain external user accounts or cloud databases, we do not store your personal information on remote servers.
* You can completely reset and erase all locally stored typing history, learned phrases, and cache at any time through Android Settings:
  > **Settings** $\rightarrow$ **Apps** $\rightarrow$ **Astral** $\rightarrow$ **Storage & Cache** $\rightarrow$ **Clear Storage**.

---

## 6. Children's Privacy

Astral is not directed to children under the age of 13. We do not knowingly collect or solicit personal information from children. If you believe your child has configured permissions or stored data on a device, you can delete this information immediately by clearing the app's local storage.

---

## 7. Changes to This Policy

We may update this Privacy Policy periodically. Any updates will be reflected on this page with an updated "Last Updated" date.

---

## 8. Contact Us

If you have any questions, concerns, or requests regarding this Privacy Policy, please contact us at:

* **Email:** [privacy@astral.app](mailto:privacy@astral.app)
* **GitHub Repository:** [https://github.com/A-Hendo/astral-assets](https://github.com/A-Hendo/astral-assets)
