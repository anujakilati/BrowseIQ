
chrome.omnibox.setDefaultSuggestion({
    description: 'Search with BrowseIQ: %s'
  });
  

  chrome.omnibox.onInputChanged.addListener((text, suggest) => {

    const suggestions = [
      { content: text + ' one', description: 'Result One for ' + text },
      { content: text + ' two', description: 'Result Two for ' + text },
      { content: text + ' three', description: 'Result Three for ' + text },
    ];
    suggest(suggestions);
  });
  
  
  chrome.omnibox.onInputEntered.addListener((text) => {
  
    const url = 'https://browseiq/search?q=' + encodeURIComponent(text);
    chrome.tabs.create({ url });
  });
  