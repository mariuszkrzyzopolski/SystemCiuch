import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class WardrobeService  {

  private apiUrl = 'http://localhost:8000/wardrobe';

  constructor(private http: HttpClient) { }

  connectToWardrobe(wardrobeCode: string) {
    const requestBody = { wardrobe_code: wardrobeCode };
    return this.http.post(`${this.apiUrl}/connect`, requestBody);
  }
}