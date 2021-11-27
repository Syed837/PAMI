import folium
import pandas as pd
import re

class plotPointOnMap:

    def __init__(self, inputPatterns, k=10, sep='\t'):
        self.inputPatterns = inputPatterns
        self.k = k
        self.sep = sep

    def findTopKPatterns(self):
        Database = []
        if isinstance(self.inputPatterns, pd.DataFrame):
            patterns = []
            i = self.inputPatterns.columns.values.tolist()
            if 'Transactions' in i:
                patterns = self.inputPatterns['Patterns'].tolist()
            for pattern in patterns:
                if isinstance(pattern, str):
                    pattern = [item for item in pattern.strip().split(self.sep)]
                Database.append(pattern)
        elif isinstance(self.inputPatterns, dict):
            for pattern in self.inputPatterns:
                if isinstance(pattern, str):
                    pattern = [item for item in pattern.strip().split(self.sep)]
                Database.append(pattern)

        elif isinstance(self.inputPatterns, str):
            with open(self.inputPatterns, 'r') as f:
                for line in f:
                    pattern = [s for s in line.strip().split(':')][0]
                    pattern = [item for item in pattern.strip().split(self.sep)]
                    Database.append(pattern)

        patterns = sorted(Database, key=lambda x: len(x[0]), reverse=True)
        # return {patternId: patterns[patternId - 1] for patternId in range(1, int(self.k) + 1)}
        return patterns[:self.k]

    def convertPOINT(self, patterns):
        locations = pd.DataFrame(columns=['patternId', 'latitude', 'longitude'])
        patternId = 1
        for pattern in patterns:
            for item in pattern:
                location = item.split(' ')
                longitude = re.sub('[^0-9. ]', '', location[0])
                latitude = re.sub('[^0-9. ]', '', location[1])
                df = pd.DataFrame([patternId, latitude, longitude], index=locations.columns).T
                locations = locations.append(df, ignore_index=True)
            patternId += 1
        return locations



    def plotPointInMap(self):
        topKPatterns = self.findTopKPatterns()
        df = self.convertPOINT(topKPatterns)
        mmap = folium.Map(location=[35.39, 139.44], zoom_start=5)
        # df = pd.read_csv(inputFile)
        colors = ['red', 'blue', 'green', 'purple', 'orange', 'darkred', 'lightred', 'beige', 'darkblue', 'darkgreen',
                  'cadetblue', 'darkpurple', 'white', 'pink', 'lightblue', 'lightgreen', 'gray', 'black', 'lightgray']
        for i, row in df.iterrows():
            folium.CircleMarker(
                location=(row['latitude'], row['longitude']),
                popup=row['patternId'],
                radius=3,
                # icon=folium.Icon(color=colors[int(row['patternId'])-1])
                color=colors[int(row['patternId']) - 1],
                fill=True,
                fill_color=colors[int(row['patternId']) - 1],
            ).add_to(mmap)
        return mmap

if __name__ == '__main__':
    obj = plotPointInMap('/Users/nakamura0803/medicalDataAnalytics/test/disease/pattern_8842163_0.8.txt')
    mmap = obj.plotPointInMap()
    mmap