// define the collapse watchdog class
class CollapseManager {
  constructor(collapse_target_id, mobile_title_id) {
    this.collapse_target = document.getElementById(collapse_target_id);
    this.mobile_title = document.getElementById(mobile_title_id);
    this.trigger = null;
    this.state = 0; // closed state.
  }

  setTrigger(trigger_id) {
    var manager = this;
    this.trigger = document.getElementById(trigger_id);
    this.trigger.addEventListener("click", function(){
      manager.toggle();
    });
  }

  toggle() {
    // if collapse_target is currently collapsed, uncollapse and add flip-image class from the trigger.
    if (this.state === 0) {
      // remove hide-mobile class from collapse_target.
      this.collapse_target.classList.remove('hide-mobile-nav');
      this.mobile_title.classList.add('hide-mobile-nav');

      //add flip-image class to trigger.
      this.trigger.classList.add("flip-image");
      this.state = 1; // uncollapsed state.
    }
    // if collapse_target is currently open, collapse and remove the flip-image class from the trigger.
    else {
      // add hide-mobile class to collapse_target.
      this.collapse_target.classList.add('hide-mobile-nav');
      this.mobile_title.classList.remove('hide-mobile-nav');

      // remove flip-image class from trigger.
      this.trigger.classList.remove('flip-image');

      this.state = 0; // uncollapsed state.
    }
  }
};
