import React, { useState, useEffect } from 'react'
import axios from 'axios';
import { Link } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';
import './plantTable.css';

function PlantTable() {
    const [plants, setPlants] = useState([]);
    const [searchText, setSearchText] = useState('');
    const [selectedCategory, setSelectedCategory] = useState('');
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();


    useEffect(() => {
        axios.get('http://localhost:8001/plants/')
            .then((response) => {
                if (response.status === 204) {
                    alert('No plants available in the database');
                    setPlants([]);
                } else {
                    setPlants(response.data);
                }
                setLoading(false);
            })
            .catch((error) => {
                console.error(error);
                setLoading(false);
            });
    }, []);
    
    if (loading) {
        return <div className="loading-container">Loading...</div>;
    }

    const categories = [...new Set(plants.map(plant => plant["Categories"]))];

    const filteredPlants = plants.filter(plant =>
        ((plant["Latin name"]).toLowerCase().includes(searchText.toLowerCase()) ||
            (plant["Family"]).toLowerCase().includes(searchText.toLowerCase())) &&
        (selectedCategory === '' || plant["Categories"] === selectedCategory)
    )

    return (
        <div className="plant-table-container">
            <div className="search-filter-container">
                <SearchBar searchText={searchText} setSearchText={setSearchText} />
                <FilterDropdown
                    categories={categories}
                    selectedCategory={selectedCategory}
                    setSelectedCategory={setSelectedCategory}
                />
            </div>
            <table className="plants-table">
                <thead>
                    <tr>
                        <th>Latin Name</th>
                        <th>Family</th>
                        <th>Category</th>
                        <th>Details</th>
                    </tr>
                </thead>
                <tbody>
                    {filteredPlants.map(plant => (
                        <PlantRow key={plant["id"]} plant={plant} navigate={navigate} />
                    ))}
                </tbody>
            </table>
        </div>
    );

}

export default PlantTable;

function PlantRow({ plant, navigate }) {
    return (
        <tr>
            <td>{plant["Latin name"]}</td>
            <td>{plant["Family"]}</td>
            <td>{plant["Categories"] || plant["category"] || 'N/A'}</td>
            <td>
                <button className="details-button" onClick={() => navigate(`/plants/${plant["id"]}`)}>More Details</button>
            </td>
        </tr>
    );
}

function SearchBar({ searchText, setSearchText }) {
    return (
        <input
            className="search-input"
            type="text"
            placeholder="Search by Latin name or Family"
            value={searchText}
            onChange={(e) => setSearchText(e.target.value)}
        />
    );
}

function FilterDropdown({ categories, selectedCategory, setSelectedCategory }) {
    return (
        <select className="filter-select" value={selectedCategory} onChange={(e) => setSelectedCategory(e.target.value)}>
            <option value="">All Categories</option>
            {categories.map((cat, index) => (
                <option key={index} value={cat}>{cat}</option>
            ))}
        </select>
    );
}