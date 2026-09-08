const defaults = Object.freeze({ necessary: true, analytics: false, marketing: false, externalMedia: false });
const listeners = new Set();
let state = defaults;

export const HIPStudioConsent = Object.freeze({
  get: () => ({ ...state }),
  allows: category => category === 'necessary' || state[category] === true,
  subscribe(callback) {
    if (typeof callback !== 'function') throw new TypeError('Consent subscriber must be a function');
    listeners.add(callback);
    return () => listeners.delete(callback);
  },
  apply(next = {}) {
    state = Object.freeze({ ...defaults, ...next, necessary: true });
    listeners.forEach(callback => callback({ ...state }));
    document.dispatchEvent(new CustomEvent('hipstudio:consent', { detail: { ...state } }));
    return { ...state };
  },
  reset() { return this.apply(defaults); }
});

window.HIPStudioConsent = HIPStudioConsent;
