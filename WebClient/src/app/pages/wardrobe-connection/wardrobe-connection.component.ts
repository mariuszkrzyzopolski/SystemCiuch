import { Component } from '@angular/core';
import { WardrobeService } from 'src/app/services/WardrobeService';

@Component({
  selector: 'app-wardrobe-connection',
  templateUrl: './wardrobe-connection.component.html',
  styleUrls: ['./wardrobe-connection.component.css']
})
export class WardrobeConnectionComponent {

  wardrobeCode: string;

  constructor(private wardrobeService: WardrobeService) { }

  connectToWardrobe() {
    this.wardrobeService.connectToWardrobe(this.wardrobeCode)
      .subscribe(
        response => {
          // Handle the response from the API
          console.log(response);
        },
        error => {
          // Handle the error
          console.error(error);
        }
      );
  }
}
