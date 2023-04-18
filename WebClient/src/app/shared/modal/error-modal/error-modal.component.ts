import { Component, EventEmitter, Input, Output } from '@angular/core';

@Component({
  selector: 'app-error-modal',
  templateUrl: './error-modal.component.html',
  styleUrls: ['./error-modal.component.css']
})
export class ErrorModalComponent {
  @Input() message: string;
  @Output() cancelEvent = new EventEmitter<void>();

  cancel() {
    this.cancelEvent.emit();
  }
}
