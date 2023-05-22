import { Component, EventEmitter, Input, Output } from '@angular/core';

@Component({
  selector: 'app-success-modal',
  templateUrl: './success-modal.component.html',
  styleUrls: ['./success-modal.component.css']
})
export class SuccessModalComponent {
  @Input() message: string;
  @Output() okEvent = new EventEmitter<void>();
  @Output() cancelEvent = new EventEmitter<void>();

  ok(){
    this.okEvent.emit();
  }

  cancel(){
    this.cancelEvent.emit();
  }
}
