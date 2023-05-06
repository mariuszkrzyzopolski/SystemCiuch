import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { DTOSet } from '../model/DTOSet';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class SetService {

   
  private readonly SETS_API_URL = 'http://localhost:8000/collection/sets';
  private readonly SET_SINGLE_API_UR = 'http://localhost:8000/collection/set';
  constructor(private http: HttpClient) { }

  addSet(firstItemId: number, secondItemId: number, thirdItemId: number) {
    const params = {
      first_item_id: firstItemId,
      second_item_id: secondItemId,
      third_item_id: thirdItemId
    };
    return this.http.post(this.SET_SINGLE_API_UR, {}, { params });
  }

  getSets() {
    return this.http.get<DTOSet[]>(this.SETS_API_URL);
  }

  deleteSet(id: number): Observable<any> {
    return this.http.delete<any>(`${this.SETS_API_URL}/${id}`);
  }
}