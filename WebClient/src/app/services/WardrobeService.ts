import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import {env} from "../app.component";

@Injectable({
  providedIn: 'root'
})
export class WardrobeService  {

  private apiUrl = env.url+'/wardrobe';

  constructor(private http: HttpClient) { }

  connectToWardrobe(wardrobeCode: string) {
    const requestBody = { wardrobe_code: wardrobeCode };
    return this.http.post(`${this.apiUrl}/connect`, requestBody);
  }

  disconnect() {
    return this.http.delete(`${this.apiUrl}/disconnect`);
  }
}