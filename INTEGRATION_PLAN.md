# Products & Use Cases Integration Plan

## Issues to Fix

### 1. Student Hub (`/ai-academy/students.html`)
- [ ] Add Products completions tracking from `aesop-ladder-products-state`
- [ ] Add Use Cases completions tracking from `aesop-ladder-use-cases-state`
- [ ] Display "Products Completed" section with count
- [ ] Display "Use Cases Completed" section with count
- [ ] Add quick links to Products and Use Cases pages
- [ ] Update hero stats to include product/use case counts

### 2. Transcript (`/ai-academy/transcript.html`)
- [ ] Add Products section showing completed products by category
- [ ] Add Use Cases section showing completed use cases by topic
- [ ] Display counts in hero stats
- [ ] Organize products/use cases similar to tier cards
- [ ] Update print functionality to include products/use cases

### 3. Navigation (All Three Pages)
- [ ] Add Products link to Student Hub nav
- [ ] Add Use Cases link to Student Hub nav
- [ ] Add Products link to Transcript nav
- [ ] Add Use Cases link to Transcript nav
- [ ] Update footer navigation consistently

## Data Sources

**Products State** (`aesop-ladder-products-state-v1`):
```javascript
{
  selectedProduct: { id, name, type },
  courseStarts: {
    [courseId]: { status: "started|completed", completedAt: timestamp }
  }
}
```

**Use Cases State** (`aesop-ladder-use-cases-state-v1`):
```javascript
{
  selectedUseCase: { id, name, topic },
  courseStarts: {
    [courseId]: { status: "started|completed", completedAt: timestamp }
  }
}
```

## Implementation Order

1. **Student Hub Updates** - Add product/use case sections
2. **Transcript Updates** - Add product/use case sections
3. **Navigation Updates** - Add links across all pages
4. **Testing** - Verify data loads and displays correctly
5. **Documentation** - Update Obsidian with changes

## Files to Modify

- `ai-academy/students.html` (v1.1.0 → v1.2.0)
- `ai-academy/transcript.html` (v1.1.0 → v1.2.0)
- Both `theladder-products/index.html` and `theladder-use-cases/index.html` if nav needs updates

## Version Bumps

- Student Hub: v1.1.0 → v1.2.0
- Transcript: v1.1.0 → v1.2.0
