import { Component } from '@angular/core';
import { WardrobeService } from 'src/app/services/WardrobeService';

@Component({
  selector: 'app-wardrobe-connection',
  templateUrl: './wardrobe-connection.component.html',
  styleUrls: ['./wardrobe-connection.component.css']
})
export class WardrobeConnectionComponent {
  wardrobeCode: string;
  showSuccess = false;
  showFailed = false;
  showDisconnect = false;
  disconnectSuccess = false;
  disconnectFailed = false;

  constructor(private wardrobeService: WardrobeService) { }

  connectToWardrobe() {
    this.wardrobeService.connectToWardrobe(this.wardrobeCode)
      .subscribe(
        response => {
          this.showSuccess = true;
          this.showDisconnect = true;
        },
        error => {
          this.showFailed = true;
          this.showDisconnect = true;
        }
      );
  }

  closeModal(){
    this.showFailed = false;
    this.showSuccess = false;
    this.disconnectSuccess = false;
    this.disconnectFailed = false;
  }

  disconnect() {
    this.wardrobeService.disconnect()
          .subscribe(
            response => {
              this.disconnectSuccess = true;
              this.showDisconnect = false;
            },
            error => {
              this.disconnectFailed = true;
            }
          );
  }
}
