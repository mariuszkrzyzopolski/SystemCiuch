import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { DTOCollection } from '../model/DTOCollection';

@Injectable({
  providedIn: 'root'
})
export class CollectionService {

  private apiUrl = 'http://localhost:8000/collection';
  private collectionUrl = 'http://localhost:8000/collection/';


  constructor(private http: HttpClient) { }

  getCollection(): Observable<DTOCollection> {
    return this.http.get<DTOCollection>(this.apiUrl);
  }

  deleteCollectionItem(id: number): Observable<any> {
    return this.http.delete<any>(`${this.apiUrl}/item/${id}`);
  }

  save(id: number, tags: string[]) {
    return this.http.patch<any>(`${this.apiUrl}/item/${id}`, {tags: tags} );
  }

  saveAutomaticSet(category: string) {
    const url = `${this.apiUrl}/ai_set/${category}`;
    return this.http.post(url, null);
  }
}