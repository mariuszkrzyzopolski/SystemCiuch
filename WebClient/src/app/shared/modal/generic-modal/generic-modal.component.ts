import { Component, EventEmitter, Input, Output } from '@angular/core';

@Component({
  selector: 'app-modal',
  templateUrl: './generic-modal.component.html'
})
export class GenericModalComponent {
  @Input() visible: boolean = false;
  @Input() cancelButton = true;
  @Output() okEvent = new EventEmitter<void>();
  @Output() cancelEvent = new EventEmitter<void>();
  
  cancel(){
    this.cancelEvent.emit();
  }

  ok(){
    this.okEvent.emit();
  }
}